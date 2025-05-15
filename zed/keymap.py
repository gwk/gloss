#!/usr/bin/env python3

import re
from dataclasses import dataclass
from json import JSONDecodeError
from sys import argv
from typing import Any

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

  defaults = parse_defaults(defaults_json_path)

  outM(defaults)


@dataclass(kw_only=True)
class Bindings:
    context: str = ''
    use_key_equivalents: bool = False
    bindings: dict[str,str|list[Any]]

transtructor = Transtructor()


def parse_defaults(defaults_path:str) -> list[Bindings]:
  # Parse the default JSON. It has comments in it, so we have to strip those out first.
  json_lines = []
  for line in open(defaults_path):
    if m := comment_re.search(line):
        line = line[:m.start()]
    json_lines.append(line)

  json_str = ''.join(json_lines)
  try: defaults = parse_json(json_str)
  except JSONDecodeError as e:
    idx = e.lineno - 1
    exit(f'{defaults_path}:{e.lineno}: error: {e}\n{json_lines[idx]}')

  return transtructor.transtruct(list[Bindings], defaults)


comment_re = re.compile(r'//.*')


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
