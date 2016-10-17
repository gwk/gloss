#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

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
