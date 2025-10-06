#!/usr/bin/env python3

import re
from collections import defaultdict
from copy import replace
from dataclasses import dataclass, field
from json import JSONDecodeError
from sys import argv
from typing import Any, Iterable

from pithy.fs import make_dirs
from pithy.io import errL, writeL
from pithy.iterable import fan_by_attr
from pithy.json import JsonDict, parse_json, write_json
from pithy.path import path_dir


'''
Parse the default VSCode keybindings, validate customzations from `keys.txt`, and output custom keybindings to json.

VSCode keybindings are complex and interact with each other in subtle ways.

This script first resets all bindings and then adds in the custom bindings.
This is desirable because I don't want unknown actions to fire if I mistakenly hit a key combination.

Default keybindings are obtained from selecting "Open Default Keyboard Shortcuts" from the command palette
and pasting them into `vscode/keybindings-default.json`.
'''


def main() -> None:
  # Paths passed in by make.
  defaults_json_path, bindings_path, out_path = argv[1:]

  out_dir = path_dir(out_path)
  make_dirs(out_dir)

  defaults_out_path = out_dir + '/keys-defaults.txt'
  clean_out_path = out_dir + '/keys-clean.txt'
  whens_out_path= out_dir + '/keys-whens.txt'
  keys_ref_out_path = out_dir + '/keys-reference.txt'

  # Parse the defaults and derive sets of names for validation.

  defaults = parse_defaults_json(defaults_json_path)

  all_cmds = set(b.cmd for b in defaults) | set(known_extension_cmds)

  nullifications = [nullification_binding(b) for b in defaults if b.key]

  dflt_specials = defaultdict[str,list[str]](list) # Maps special key to commands bound to it. Use lists to preserve order.
  dflt_binding_whens = defaultdict[str,set[str]](set) # Maps command name to list of default 'when' clauses.
  all_when_words = set[str]()

  for b in defaults:
    if b.key in special_keys:
      dflt_specials[b.key].append(b.cmd)

    if when := b.when:
      dflt_binding_whens[b.cmd].add(when)
      for word in when.split():
        all_when_words.add(word.lstrip('!'))

  write_keys_txt(defaults_out_path, defaults)
  write_whens(whens_out_path, all_when_words)

  # Set up context for parsing.
  ctx = Ctx(
    bindings_path=bindings_path,
    defaults=defaults,
    all_cmds=all_cmds,
    dflt_binding_whens=dflt_binding_whens,
    all_when_words=all_when_words)

  # Parse and validate the custom bindings.

  bindings = parse_bindings(ctx, bindings_path)

  cmd_bindings:dict[str,list[Binding]] = fan_by_attr(bindings, 'cmd')
  for cmd, cmd_bs in cmd_bindings.items():
    validate_whens_list(ctx, cmd, cmd_bs)

  bound_specials = defaultdict[str,set[str]](set)
  for b in bindings:
    if b.key in special_keys:
      bound_specials[b.key].add(b.cmd)

  detect_unbound_cmds(all_cmds, ctx.bound_cmds, dflt_specials, bound_specials)

  # Output the custom bindings and reference files.

  write_keys_txt(clean_out_path, bindings)
  write_bindings_json(out_path, nullifications, bindings)
  write_keys_ref(keys_ref_out_path, bindings)


@dataclass(frozen=True)
class Binding:
  cmd:str
  key:str
  line_num:int = 0
  when:str = ''
  args:dict[str,str]|None = None

  def json(self) -> dict[str,str|dict[str,str]]:
    d:dict[str,str|dict[str,str]] = dict(key=self.key, command=self.cmd)
    if self.when: d['when'] = self.when
    if self.args: d['args'] = self.args
    return d


special_keys = ('enter', 'escape', 'tab') # Handle bindings to these keys specially.
#^ These often have many bindings, sometimes to the same command but with different complex 'when' clauses.
#^ Furthermore, order appears to matter for bindings, which makes these keys especially tricky.
#^ Binding names change over time and various aspects of the UI are not usable without these bindings.
#^ It can be difficult to discover the name of a binding when it breaks.


def parse_defaults_json(defaults_path:str) -> list[Binding]:
  '''
  Parse the default JSON. It has comments in it, some of which are the "other available commands".
  Thus we have to preprocess the comments first.
  This function preserves the ordering of the input bindings.
  '''
  json_lines = []
  other_cmds = [] # Commands suggested by "Here are other available commands:" comment at end of the defaults file.
  comment_re = re.compile(r'\s*//\s*(-)?\s*(.*)')
  other_command_trailing_junk_re = re.compile(r'(-#\d+-.+)$')
  #^ As of 2024-07, some extension commands have a weird "-#1-" followed by the extension description, which includes spaces.
  for line in open(defaults_path):
    m = comment_re.match(line) # For now, only recognize comments on their own line.
    if m: # Commented line.
      json_lines.append(line[:m.start()]) # Preserve line numbers for json parser.
      if m[1]: # Contains dash; assume one of the "other available commands."
        cmd = m[2].strip()
        if junk_m := other_command_trailing_junk_re.search(cmd):
          print("note: stripped junk from commented command:", cmd)
          cmd = cmd[:junk_m.start()]
        assert cmd
        other_cmds.append(cmd)
    else:
      json_lines.append(line)

  # Parse the filtered json.
  json_str = ''.join(json_lines)
  try: defaults_json = parse_json(json_str)
  except JSONDecodeError as e:
    idx = e.lineno - 1
    exit(f'{defaults_path}:{line}: error: {e}\n{json_lines[idx]}')


  def clean_when(when:str) -> str: return ' '.join(when.split())

  defaults = [
    Binding(cmd=d['command'], key=d['key'],when=clean_when(d.get('when', '')), args=d.get('args')) for d in defaults_json]

  for cmd in other_cmds:
    defaults.append(Binding(cmd=cmd, key=''))

  return defaults


def nullification_binding(binding:Binding) -> JsonDict:
  return {
    'key': binding.key,
    'command': '-' + binding.cmd
  }


def fmt_key_line(binding:Binding) -> str:
  cmd = binding.cmd
  key = binding.key
  when = binding.when
  args = binding.args
  assert not re.search(r':( |$)', cmd), cmd # Check to make sure our delimiter is not ambiguous; see `parse_binding`.
  if ' ' in cmd: cmd += ':' # Add a trailing colon delimiter to disambiguate commands with spaces.
  when_clause = fmt_when(when)
  args_clause = f' {args}' if args else ''
  return f'{cmd:<79} {key:15} {when_clause}{args_clause}'.rstrip()


def fmt_when(when:str) -> str:
  return f'when {when}' if when else ''


def write_keys_txt(path:str, bindings:list[Binding]) -> None:
  'Generate a keybindings text file.'
  f = open(path, 'w')
  for binding in sorted(bindings, key=lambda b: (b.cmd.lower(), b.key, b.when)):
    f.write(fmt_key_line(binding) + '\n')


def write_whens(path:str, all_when_words:set[str]) -> None:
  with open(path, 'w') as f:
    for when in sorted(all_when_words, key=lambda word: (word.isalnum(), word)):
      writeL(f, when)


@dataclass(frozen=True)
class Ctx:
  bindings_path: str
  defaults: list[Binding]
  all_cmds: set[str]
  dflt_binding_whens: defaultdict[str,set[str]]
  all_when_words: set[str]
  bound_cmds: set[str] = field(default_factory=set)

  def _msg(self, line:int, severity:str, item:Any, *items:Any, sep=' '):
    errL(f'{self.bindings_path}:{line}: {severity}: {item}', *items, sep=sep)

  def warn(self, line:int, item:Any, *items:Any, sep=' '):
    self._msg(line, 'warning', item, *items, sep=sep)

  def error(self, line:int, item:Any, *items:Any, sep=' '):
    self._msg(line, 'error', item, *items, sep=sep)
    exit(1)


def write_bindings_json(path:str, nullifications:list[JsonDict], bindings:list[Binding]) -> None:
  '''
  Write the bindings to a json file.
  Note: we omit all tab bindings because of weird problems with Cursor.
  '''
  output_bindings = [b.json() for b in bindings if b.key and b.key != 'tab']
  with open(path, 'w') as f: write_json(f, output_bindings)


def write_keys_ref(path:str, bindings:list[Binding]) -> None:
  explicit_bindings = [b for b in bindings if b.key]
  with open(path, 'w') as f:
    for binding in sorted(explicit_bindings, key=bindings_sort_key):
      cmd = binding.cmd
      key = binding.key
      when = binding.when
      when = f' when {binding.when}' if binding.when else ''
      args = f' {binding.args}' if binding.args else ''

      print(f'{key:24} {cmd:64}{when}{args}', file=f)


def bindings_sort_key(binding:Binding) -> list[bool|str]:
  key_combo = binding.key.split('+')
  key_combo.reverse()
  is_regular_key = (len(key_combo[0]) == 1)
  return [is_regular_key] + key_combo


def parse_bindings(ctx:Ctx, bindings_path:str) -> list[Binding]:
  bindings = []
  for line_num, line in enumerate(open(bindings_path), 1):
    if not line.strip(): continue
    if line.startswith('//'): continue
    if b := parse_binding(ctx, line_num, line):
      bindings.append(b)
  return bindings


def parse_binding(ctx:Ctx, line_num:int, line:str) -> Binding|None:
  if line[0].isspace(): ctx.error(line_num, 'line begins with space.')
  line = line.rstrip()

  # Find the command name at the start of the line.
  # Some command names have spaces in them so we delimit them with a colon.
  if m := re.search(r':( |$)', line):
    cmd = line[:m.start()]
    words = [cmd] + line[m.end():].split()
  else:
    words = line.split()
    cmd = words[0]

  try:
    when_index = words.index('when')
  except ValueError:
    keys = words[1:]
    when_words:list[str] = []
  else:
    keys = words[1:when_index]
    when_words = words[when_index+1:]
  when = ' '.join(when_words)
  ctx.bound_cmds.add(cmd)

  if not validate_cmd(ctx, line_num, cmd=cmd): return None # Omit unknown commands.
  validate_keys(ctx, line_num, keys=keys)

  if keys: validate_when(ctx, line_num, cmd=cmd, when=when, when_words=when_words)

  key = ' '.join(keys)

  return Binding(cmd=cmd, key=key, line_num=line_num, when=when)


def validate_cmd(ctx:Ctx, line_num:int, cmd:str) -> bool:
  if cmd not in ctx.all_cmds:
    ctx.warn(line_num, 'unknown command:', cmd)
    return False
  return True


def validate_keys(ctx:Ctx, line_num:int, keys:Iterable[str]):
  for word in keys:
    for el in word.split('+'):
      if not key_validator.fullmatch(el):
        ctx.error(line_num, f'bad key: {el!r}')


def validate_when(ctx:Ctx, line_num:int, cmd:str, when:str, when_words:list[str]) -> None:
  for word in when_words:
    if word.lstrip('!') not in ctx.all_when_words and word not in known_when_words:
      ctx.warn(line_num, f'bad when word: {word}')


def validate_whens_list(ctx:Ctx, cmd:str, bindings:list[Binding]) -> None:
  if not any(b.key for b in bindings): return # No bound keys.

  dflt_whens_unaltered = ctx.dflt_binding_whens.get(cmd, set())
  if not dflt_whens_unaltered: return # No default whens to compare against.

  when_alterations = known_when_alterations.get(cmd, {})
  dflt_whens = {when_alterations.get(w, w) for w in dflt_whens_unaltered}

  covered_whens = set()

  has_problem = False

  for b in bindings:
    if b.when not in dflt_whens:
      ctx.warn(b.line_num, f'mismatched when for command: {cmd}',
        f'gloss: {fmt_when(b.when)}',
        *[fmt_key_line(replace(b, when=dw)) for dw in dflt_whens],
        sep='\n')
      has_problem = True
    else:
      covered_whens.add(b.when)

  if missing_whens := dflt_whens - covered_whens:
    ctx.warn(bindings[-1].line_num, f'missing whens for command: {cmd}',
      *[fmt_key_line(replace(bindings[0], when=dw)) for dw in missing_whens],
      sep='\n')
    has_problem = True

  if has_problem: errL()


def detect_unbound_cmds(all_cmds:set[str], bound_cmds:set[str], dflt_specials:defaultdict[str,list[str]],
 bound_specials:defaultdict[str,set[str]]) -> None:

  if unbound_cmds := all_cmds - bound_cmds:
    errL('\nunbound commands:')
    for cmd in sorted(unbound_cmds):
      errL(fmt_key_line(Binding(cmd=cmd, key='')))

  for key in special_keys:
    if unbound := [cmd for cmd in dflt_specials[key] if cmd not in bound_specials[key]]:
      errL(f'\nunbound {key!r} commands:')
      for cmd in sorted(unbound):
        errL(fmt_key_line(Binding(cmd=cmd, key=key)))

  errL()


# https://code.visualstudio.com/docs/getstarted/keybindings#_accepted-keys
key_validator = re.compile(r'''(?x)
  alt
| cmd
| ctrl
| escape
| shift
| space | backspace | delete | enter | tab
| up | down | left | right
| pageup| pagedown | home | end
| f(?:\d{1,2})
| \\?[][-zA-Z0-9\'"`.,;/\\=-]
''')


known_custom_when_cmds = {
  'undo',
  'editor.action.acceptCursorTabSuggestion',
  'workbench.action.reloadWindow',
  'inlineChat.hideHint',
}


known_when_words = {
  'inlineChatShowingHint',
}


known_when_alterations:dict[str,dict[str,str]] = {
  'workbench.action.reloadWindow': {'isDevelopment' : ''}
}


known_extension_cmds = {
  'settings.cycle.trimTrailingWhitespace',
}

main()
