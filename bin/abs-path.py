#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from os.path import abspath, expanduser
from shlex import quote
from sys import argv


for p in argv[1:]:
  s = abspath(expanduser(p))
  print(quote(s))
