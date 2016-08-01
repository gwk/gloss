#!/usr/bin/env python3
# Copyright 2011 George King. Permission to use this file is granted in license-gloss.txt.

from sys import argv
from shlex import quote
from os.path import abspath, expanduser

for p in argv[1:]:
  s = abspath(expanduser(p))
  print(quote(s))
