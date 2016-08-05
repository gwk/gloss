#!/usr/bin/env python3
# Copyright 2013 George King. Permission to use this file is granted in license-gloss.txt.


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
