#!/usr/bin/env python3
# Copyright 2009 George King. Permission to use this file is granted in license-gloss.txt.

# print the last argument

import sys

if len(sys.argv) < 2:
  print('last_arg error: no arguments', file=sys.stderr)
  sys.exit(1)

print(sys.argv[-1])
