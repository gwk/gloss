#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from sys import argv, stdin, stdout
from json import JSONDecoder, dump


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
  extra = s[end_index:]
  if not extra.isspace():
    snippet = extra[:64]
    tail = '…' if len(extra) > 64 else ''
    exit(f'extraneous input beginning at offset {end_index}:\n{snippet!r}')
