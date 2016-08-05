#!/usr/bin/env python3
# Copyright 2013 George King. Permission to use this file is granted in license-gloss.txt.

import sys
import json
import plistlib

args = sys.argv[1:]

if not (1 <= len(args) <= 2):
  print('usage: input-path output-path=stdout', file=sys.stderr)
  sys.exit(1)

f_in = open(args[0])
f_out = open(args[1], 'wb') if len(args) == 2 else sys.stdout.detach() # get binary file.

obj = json.load(f_in)
plistlib.dump(obj, f_out)
