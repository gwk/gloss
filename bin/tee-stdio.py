#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.


import sys

flags = sys.argv[1:]

label = ('-label' in flags)

for line in sys.stdin:
  if label:
    sys.stdout.write('out: ')
  sys.stdout.write(line)
  if label:
    sys.stderr.write('err: ')
  sys.stderr.write(line)
