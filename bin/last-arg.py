#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# print the last argument.

from import sys import argv


if len(argv) < 2:
  exit('last_arg error: no arguments')

print(sys.argv[-1])
