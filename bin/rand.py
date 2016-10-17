#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# generate a random numeric string.

import sys
import random


if len(sys.argv) != 2:
  print("usage: rand limit", file=sys.stderr)
  sys.exit(1)

l = int(sys.argv[1])
r = random.randint(0, l)
print(r)
