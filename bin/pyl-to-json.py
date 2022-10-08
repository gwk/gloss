#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import json
import sys
from argparse import ArgumentParser, FileType
from ast import literal_eval


def main() -> None:
  parser = ArgumentParser(description="Convert python literal files to JSON.")
  parser.add_argument('input', type=FileType('r'), help='input .pyl file path')
  parser.add_argument('output', nargs='?', type=FileType('w'), default='-',
    help="output .json file path (defaults to '-', indicating stdout)")
  parser.add_argument('-indent', type=int, default=2, help='json indentation')
  parser.add_argument('-compact', action='store_true', help='output compact json (ignores indent)')

  args = parser.parse_args()

  f_in = args.input
  f_out = args.output

  obj = literal_eval(f_in.read())

  if args.compact:
    indent = None
    seps = (',', ':')
  else:
    indent = args.indent
    seps = None
  json.dump(obj, f_out, sort_keys=True, indent=indent, separators=seps)
  f_out.write('\n')


if __name__ == '__main__': main()
