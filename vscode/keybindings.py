#!/usr/bin/env python3

import re
from sys import argv
from pithy.fs import make_dirs
from pithy.io import errL, errSL, errLL, outL, writeL
from pithy.iterable import group_by_heads
from pithy.json import JSONDecodeError, parse_json, write_json
from pithy.path import path_dir, path_stem
from dataclasses import dataclass, field
from typing import Any, DefaultDict, Dict, Iterable, List, Set, Tuple


'''
Parse the default VSCode keybindings, validate customzations from `keys.txt`, and output custom keybindings to json.

VSCode keybindings are complex and interact with each other in subtle ways.

This script first resets all bindings and then adds in the custom bindings.
This is desirable because I don't want unknown actions to fire if I mistakenly hit a key combination.
However it appears that order of bindings matters for complicated bindings, particularly the tab key.
To mitigate this we ignore tab key bindings in both the nullifications and the custom bindings.
Tab bindings still appear in the keys file and are checked against the defaults.
Obviously this leaves something to be desired but is the path of least resistance for now.

Default keybindings are obtained from selecting "Open Default Keyboard Shortcuts" from the command palette
and pasting them into the default JSON file in `vscode/`.
'''


def main() -> None:
  # Paths passed in by make.
  defaults_json_path, bindings_path, out_path = argv[1:]

  out_dir = path_dir(out_path)
  make_dirs(out_dir)

  out_stem = path_stem(out_path)
  defaults_out_path = out_dir + '/keys-defaults.txt'
  whens_out_path= out_dir + '/keys-whens.txt'
  keys_ref_out_path = out_dir + '/keys-reference.txt'

  defaults, other_cmds = parse_defaults(defaults_json_path)

  ctx = Ctx(
    bindings_path=bindings_path,
    defaults=defaults,
    other_cmds=other_cmds,
    all_cmds=set(known_extension_cmds))

  write_defaults_txt(defaults_out_path, ctx.dflt_triples)
  write_whens(whens_out_path, ctx.all_when_words)

  parse_bindings(ctx, bindings_path)
  warn_unbound_cmds(ctx)

  write_bindings(ctx, out_path)
  write_keys_ref(keys_ref_out_path, ctx.bindings)


Binding = Dict[str,str]
Triple = Tuple[str,str,str]


def parse_defaults(defaults_path:str) -> Tuple[List[Binding],List[str]]:
  # Parse the default JSON. It has comments in it, so we have to strip those out first.
  json_lines = []
  other_cmds = [] # Commands suggested by "Here are other available commands:" comment at end of the defaults file.
  comment_re = re.compile(r'\s*//\s*(-)?\s*(.*)')
  for line in open(defaults_path):
    m = comment_re.match(line) # For now, only recognize comments on their own line.
    if m: # Commented line.
      json_lines.append(line[:m.start()]) # Preserve line numbers for json parser.
      if m[1]: # Contains dash; assume one of the "other available commands."
        cmd = m[2].strip()
        assert cmd
        other_cmds.append(cmd)
    else:
      json_lines.append(line)

  # Parse the filtered json.
  json_str = ''.join(json_lines)
  try: defaults = parse_json(json_str)
  except JSONDecodeError as e:
    idx = e.lineno - 1
    exit(f'{defaults_path}:{line}: error: {e}\n{json_lines[idx]}')
  return defaults, other_cmds


@dataclass(frozen=True)
class Ctx:
  bindings_path: str
  defaults: List[Binding]
  other_cmds: List[str] # Commands that are not bound by default.
  all_cmds: Set[str]

  all_when_words: Set[str] = field(default_factory=set)
  dflt_binding_whens: Dict[str,Set[str]] = field(default_factory=lambda:DefaultDict(set))
  dflt_escapes: Set[str] = field(default_factory=set)
  dflt_tabs: Set[str] = field(default_factory=set)
  dflt_triples: List[Triple] = field(default_factory=list)

  bindings: List[Dict[str,str]] = field(default_factory=list) # Includes nullifications.
  bound_cmds: Set[str] = field(default_factory=set)
  bound_escapes: Set[str] = field(default_factory=set)
  bound_tabs: Set[str] = field(default_factory=set)


  def msg(self, line:int, *items:Any):
    errSL(f'{self.bindings_path}:{line}:', *items)


  def warn(self, line:int, *items:Any): self.msg(line, 'warning:', *items)


  def error(self, line:int, *items:Any):
    self.msg(line, 'error:', *items)
    exit(1)


  def __post_init__(self) -> None:
    # Nullify each default by adding a matching rule with a negating command.
    # Additionally, accumulate all cmds and whens.
    for dflt in self.defaults:
      key = dflt['key']
      cmd = dflt['command']
      self.all_cmds.add(cmd)
      nullification = {
        'key': key,
        'command': '-' + cmd
      }
      if key == 'escape':
        self.dflt_escapes.add(cmd)
      if key == 'tab':
        self.dflt_tabs.add(cmd)

      when_words = dflt.get('when', '').split()
      when = ' '.join(when_words)
      self.dflt_binding_whens[cmd].add(when)
      if when:
        # Note: as of 2018/08/03, do not qualify nullifications with when clauses, or else they will fail in some cases.
        for word in when.split():
          self.all_when_words.add(word.lstrip('!'))
      self.bindings.append(nullification)
      self.dflt_triples.append((cmd, key, when))

    for cmd in self.other_cmds:
      self.all_cmds.add(cmd)
      self.dflt_triples.append((cmd, '', ''))



def write_defaults_txt(path:str, dflt_triples:List[Triple]) -> None:
  'Generate keybindings.txt as starting point for customization.'
  f = open(path, 'w')
  for (cmd, key, when) in sorted(dflt_triples):
    if ' ' in cmd: cmd += ':' # Add a trailing colon delimiter to disambiguate commands with spaces.
    when_clause = f'when {when}' if when else ''
    writeL(f, f'{cmd:<79} {key:15} {when_clause}'.strip())


def write_whens(path:str, all_when_words:Set[str]) -> None:
  with open(path, 'w') as f:
    for when in sorted(all_when_words):
      writeL(f, when)


def write_bindings(ctx:Ctx, out_path:str) -> None:
  output_bindings = [b for b in ctx.bindings if b['key'] != 'tab']
  with open(out_path, 'w') as f: write_json(f, output_bindings)


def write_keys_ref(path:str, bindings:list[dict[str,str]]) -> None:
  explicit_bindings = [b for b in bindings if b['key']]
  with open(path, 'w') as f:
    for binding in sorted(explicit_bindings, key=bindings_sort_key):
      key = binding['key']
      cmd = binding['command']
      when = binding.get('when', '')
      s = when and ' '
      print(f'{key:24} {cmd:64}{s}{when}', file=f)


def bindings_sort_key(binding:Dict[str,str]) -> List[str]:
  key_combo = binding['key'].split('+')
  key_combo.reverse()
  is_regular_key = (len(key_combo[0]) == 1)
  return [is_regular_key] + key_combo


def parse_bindings(ctx:Ctx, bindings_path:str) -> None:
  for line_num, line in enumerate(open(bindings_path), 1):
    parse_binding(ctx, line_num, line)


def parse_binding(ctx:Ctx, line_num:int, line:str) -> None:
  line = line.rstrip()
  if not line.strip(): return # Empty line.
  if line[0].isspace(): ctx.error(line_num, 'line begins with space.')
  if line.startswith('//'): return

  # Find the command name at the start of the line.
  # Some command names have spaces in them so we delimit them with a colon.
  if m := re.search(r':( |$)', line):
    cmd = line[:m.start()]
    words = [cmd] + line[m.end():].split()
  else:
    words = line.split()
    cmd = words[0]

  if cmd not in ctx.all_cmds:
    ctx.warn(line_num, 'unknown command:', cmd)
  try:
    when_index = words.index('when')
  except ValueError:
    keys = words[1:]
    when_words:List[str] = []
  else:
    keys = words[1:when_index]
    when_words = words[when_index+1:]
  when = ' '.join(when_words)
  ctx.bound_cmds.add(cmd)

  if not keys: return

  validate_keys(ctx, line_num, keys=keys)
  validate_when(ctx, line_num, cmd=cmd, when=when, when_words=when_words)

  def add_binding(key:str) -> None:
    binding = {
      'command': cmd,
      'key': key,
    }
    if when_words:
      binding['when'] = when

    # Originally this supported multiline bindings with subsequent lines indented, containing `args` in json synatx.
    # However over time I came to rely on sorting the whole file by lines in order to update it when new bindings were added to VSCode.
    args = None
    if args is not None:
      binding['args'] = args
    ctx.bindings.append(binding)

  key = ' '.join(keys)
  add_binding(key)
  if key == 'escape':
    ctx.bound_escapes.add(cmd)
    add_binding('ctrl+c')
  if key == 'tab':
    ctx.bound_tabs.add(cmd)


def validate_keys(ctx:Ctx, line_num:int, keys:Iterable[str]):
  for word in keys:
    for el in word.split('+'):
      if not key_validator.fullmatch(el):
        ctx.error(line_num, f'bad key: {el!r}')

def validate_when(ctx:Ctx, line_num:int, cmd:str, when:str, when_words:List[str]) -> None:
  default_whens = ctx.dflt_binding_whens[cmd]
  if default_whens and when not in default_whens:
    ctx.msg(line_num, f'note: custom when for command: {cmd}\n  gloss:   {when}', *[f'\n  default: {dflt}' for dflt in default_whens])
  for word in when_words:
    if word.lstrip('!') not in ctx.all_when_words:
      ctx.error(line_num, f'bad when word: {word}')


def warn_unbound_cmds(ctx:Ctx) -> None:
  if unbound_cmds := ctx.all_cmds - ctx.bound_cmds:
    errLL('\nunbound commands:', *sorted(unbound_cmds))

  if unbound_escapes := ctx.dflt_escapes - ctx.bound_escapes:
    errLL('\nunbound escapes:', *sorted(unbound_escapes))

  if unbound_tabs := ctx.dflt_tabs - ctx.bound_tabs:
    errLL('\nunbound tabs:', *sorted(unbound_tabs))

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

known_extension_cmds = {
  'settings.cycle.trimTrailingWhitespace',
}

main()
