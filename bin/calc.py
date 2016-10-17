#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# print the results of evaluating each argument as a python expression.

import sys
import math
import random
import pprint


env = {}

def add(module, name):
  env[name] = getattr(module, name)

add(pprint, 'pprint')

for m in [math, random]:
  for n in dir(m):
    if not n.startswith('_'):
      add(m, n)

for expr in sys.argv[1:]:
  try:
    val = eval(expr, env)
    if val is not None:
      print(val)
  except Exception as e:
    print('error in expression:', e, file=sys.stderr)
