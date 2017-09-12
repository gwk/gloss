#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from sys import argv, stdin, stdout
from json import JSONDecoder, dump

from pithy.io import errL


if len(argv) > 2:
  exit('requires 1 or no arguments (defaults to std-in)')

if len(argv) == 2:
  f = open(argv[1])
else:
  f = stdin

s = f.read()
o, end_index = JSONDecoder(strict=False).raw_decode(s)

dump(o, stdout, sort_keys=True, indent=2)
stdout.write('\n')

if end_index < len(s):
  tail = '…' if end_index + 64 < len(s) else ''
  errL(f'extraneous input beginning at offset {end_index}:\n', s[end_index:end_index + 64].encode('utf8'), tail)
