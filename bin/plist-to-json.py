#!/usr/bin/env python3
# Copyright 2013 George King. Permission to use this file is granted in license-gloss.txt.

import sys
import json
import plistlib

args = sys.argv[1:]

if not (1 <= len(args) <= 2):
  print('usage: input-path output-path=stdout', file=sys.stderr)
  sys.exit(1)

f_in = open(args[0], 'rb')
f_out = open(args[1], 'w') if len(args) == 2 else sys.stdout

obj = plistlib.load(f_in)
json.dump(obj, f_out, sort_keys=True, indent=2)
f_out.write('\n')
