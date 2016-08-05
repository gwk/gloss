#!/usr/bin/env python3
# Copyright 2009 George King. Permission to use this file is granted in license-gloss.txt.

# generate a random numeric string


import sys
import random


if len(sys.argv) != 2:
  print("usage: rand limit", file=sys.stderr)
  sys.exit(1)

l = int(sys.argv[1])
r = random.randint(0, l)
print(r)
