#!/usr/bin/env python3

import re
from sys import argv
from pithy.fs import path_stem
from pithy.io import errL, errSL, outL, writeL
from pithy.iterable import group_by_heads
from pithy.json import JSONDecodeError, parse_json, write_json
from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Set, Tuple

'''
Parse the default VSCode keybindings, validate custom ones, and install them.
Default keybindings are obtained from selecting "Open Default Keyboard Shortcuts" from the command palette
and pasting them into the default JSON file in `vscode/`.
'''


def main() -> None:
  # Paths passed in by make.
  defaults_json_path, bindings_path, out_path = argv[1:]

  defaults_out_path = "_build/vscode-keys-defaults.txt"
  whens_out_path= "_build/vscode-whens.txt"
  defaults, other_cmds = parse_defaults(defaults_json_path)

  ctx = Ctx(
    bindings_path=bindings_path,
    defaults=defaults,
    other_cmds=other_cmds,
    all_cmds=set(known_extension_cmds))

  write_defaults_txt(defaults_out_path, ctx.dflt_triples)
  write_whens(whens_out_path, ctx.all_whens)
  parse_bindings(ctx, bindings_path)
  warn_unbound_cmds(ctx)

  out_file = open(out_path, 'w')
  write_json(out_file, ctx.bindings)


Binding = Dict[str,str]
Triple = Tuple[str,str,str]


def parse_defaults(defaults_path:str) -> Tuple[List[Binding],List[str]]:
  # Parse the default JSON. It has comments in it, so we have to strip those out first.
  json_lines = []
  other_cmds = []
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
  other_cmds: List[str]
  all_cmds: Set[str]
  all_whens: Set[str] = field(default_factory=set)
  dflt_triples: List[Triple] = field(default_factory=list) # used to generate keybindings.txt once.
  bindings: List[Dict[str,str]] = field(default_factory=list)
  bound_cmds: Set[str] = field(default_factory=set)

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
      when = dflt.get('when', '')
      if when:
        for word in when.split():
          self.all_whens.add(word.lstrip('!'))
        #nullification['when'] = when # Disabled; causes nullification to fail in some cases.
      self.bindings.append(nullification)
      self.dflt_triples.append((cmd, key, when))
    for cmd in self.other_cmds:
      self.all_cmds.add(cmd)
      self.dflt_triples.append((cmd, '', ''))


def write_defaults_txt(path:str, dflt_triples:List[Triple]) -> None:
  'Generate keybindings.txt as starting point for customization.'
  f = open(path, 'w')
  for (cmd, key, when) in sorted(dflt_triples):
    when_clause = f'when {when}' if when else ''
    writeL(f, f'{cmd:<63} {key:23} {when_clause}'.strip())


def write_whens(path:str, all_whens:Set[str]) -> None:
  f = open(path, 'w')
  for when in sorted(all_whens):
    writeL(f, when)


def parse_bindings(ctx:Ctx, bindings_path:str) -> None:
  numbered_lines = enumerate(open(bindings_path), 1)
  for lines in group_by_heads(numbered_lines, is_head=lambda p: not p[1].startswith(' ')):
    parse_binding(ctx, lines)


def parse_binding(ctx:Ctx, binding:List[Tuple[int,str]]) -> None:
  line_num, line = binding[0] # first line.
  words = line.split()
  if not words: return
  cmd = words[0]
  if cmd.startswith('//'): return
  if cmd not in ctx.all_cmds:
    ctx.warn(line_num, 'unknown command:', cmd)
  try:
    when_index = words.index('when')
  except ValueError:
    keys = words[1:]
    whens:List[str] = []
  else:
    keys = words[1:when_index]
    whens = words[when_index+1:]
  ctx.bound_cmds.add(cmd)
  if not keys: return
  validate_keys(ctx, line_num, keys)
  validate_whens(ctx, line_num, whens)

  if len(binding) == 1:
    args = None
  else:
    args_str = ''.join(l for i, l in binding[1:])
    try: args = parse_json(args_str)
    except JSONDecodeError as e:
      ctx.error(line_num, f'invalid args JSON: {e}\n{args_str}')

  def add_binding(keys:Iterable[str]) -> None:
    binding = {
      'command': cmd,
      'key': ' '.join(keys)
    }
    if whens:
      binding['when'] = ' '.join(whens)
    if args is not None:
      binding['args'] = args
    ctx.bindings.append(binding)

  add_binding(keys)
  if keys == ['escape']: add_binding(['ctrl+c'])


def validate_keys(ctx:Ctx, line_num:int, keys:Iterable[str]):
  for word in keys:
    for el in word.split('+'):
      if not key_validator.fullmatch(el):
        ctx.error(line_num, f'bad key: {el!r}')

def validate_whens(ctx:Ctx, line_num:int, whens:Iterable[str]) -> None:
  for when in whens:
    if when.lstrip('!') not in ctx.all_whens:
      ctx.error(line_num, f'bad when: {when}')


def warn_unbound_cmds(ctx:Ctx) -> None:
  unbound = ctx.all_cmds - ctx.bound_cmds
  if not unbound: return
  errL('\nunbound commands:')
  for cmd in sorted(unbound):
    errL(cmd)
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
