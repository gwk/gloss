#!/usr/bin/env python3
# Copyright 2009 George King. Permission to use this file is granted in license-gloss.txt.

# generate a random alphanumeric string


import sys
import random


if len(sys.argv) != 2:
  print("usage: randans length", file=sys.stderr)
  sys.exit(1)

l = int(sys.argv[1])
 
for i in range(l):
  r = random.randint(0, 61)

  if r < 10:    o = 0x30      # 0-9
  elif r < 36:  o = 0x41 - 10 # A-Z
  else:         o = 0x61 - 36 # a-z
  
  print(chr(o + r), end='')

print()
