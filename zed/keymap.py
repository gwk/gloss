#!/usr/bin/env python3

import re
from dataclasses import dataclass, field
from json import JSONDecodeError
from sys import argv
from typing import Any, Callable, Iterator

from pithy.fs import make_dirs
from pithy.io import outM
from pithy.json import parse_json
from pithy.path import path_dir
from pithy.transtruct import Transtructor


'''
Parse the default Zed keybindings and validate the custom keybindings.
Default keybindings are obtained from selecting "zed: open default keymap" from the command palette
and pasting them into `zed/keybindings-default.json`.
'''


def main() -> None:
  # Paths passed in by make.
  defaults_json_path, bindings_path, out_path = argv[1:]

  out_dir = path_dir(out_path)
  make_dirs(out_dir)

  defaults = parse_zed_keymap(defaults_json_path)

  #outM(defaults)
  binding_descs = []
  for bindings in defaults:
    binding_descs.extend(bindings.fmt_bindings(by_key=True))

  binding_descs.sort()
  for bd in binding_descs:
    print(bd)

@dataclass
class Cmd:
  id:str
  arg:Any = None


@dataclass(kw_only=True)
class Bindings:
  context: str = ''
  use_key_equivalents: bool = False
  bindings: dict[str,Cmd]

  def __post_init__(self):
    self.bindings = {rectify_keybinding(k): v for k, v in self.bindings.items()}


  def fmt_bindings(self, by_key:bool) -> Iterator[str]:
    l = self.by_key() if by_key else self.by_cmd()
    for a, b, arg, ctx in l:
      ctx_str = f'  {ctx}' if ctx else ''
      arg_str = '' if arg is None else repr(arg)
      yield f'{a:38}  {b:38}  {arg_str:54}  {ctx_str}'


  def by_cmd(self) -> list[tuple[str,str,Any,str]]:
    return sorted((cmd.id, key, cmd.arg, self.context) for key, cmd in self.bindings.items())


  def by_key(self) -> list[tuple[str,str,Any,str]]:
    return sorted((key, cmd.id, cmd.arg, self.context) for key, cmd in self.bindings.items())


transtructor = Transtructor()

@transtructor.prefigure(Cmd)
def prefigure_Cmd(class_:type, input:Any, ctx:None) -> tuple[str,Any]:
  if input is None: return ('', None)
  if isinstance(input, str): return (input, None)
  if isinstance(input, list):
    if len(input) == 2: return tuple(input)
  raise ValueError(input)


def parse_zed_keymap(path:str) -> list[Bindings]:
  # Parse the default JSON. It has comments in it, so we have to strip those out first.
  json_lines = []
  for line in open(path):
    if m := comment_re.search(line):
        line = line[:m.start()]
    json_lines.append(line)

  json_str = ''.join(json_lines)
  try: defaults = parse_json(json_str)
  except JSONDecodeError as e:
    idx = e.lineno - 1
    exit(f'{path}:{e.lineno}: error: {e}\n{json_lines[idx]}')

  return transtructor.transtruct(list[Bindings], defaults)


comment_re = re.compile(r'//.*')


def rectify_keybinding(keybinding:str) -> str:
  return ' '.join(rectify_key(key) for key in keybinding.split())


def rectify_key(key:str) -> str:
  if m := re.search(r'-+$', key):
    if m.group() != '--':
      print('WARNING: key has odd trailing dashes:', key)
      return key
    key = key.removesuffix('--')
    trail_dashes = '--'
  else:
    trail_dashes = ''

  parts = key.split('-')
  parts.sort(key=lambda part: mod_key_sort_order.get(part, part))
  return '-'.join(parts) + trail_dashes


mod_key_sort_order = {
  '' : '\xff',
  'cmd' : '\x00',
  'ctrl' : '\x01',
  'alt' : '\x02',
  'shift' : '\x03',
}


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


main()
