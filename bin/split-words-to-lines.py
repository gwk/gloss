#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import sys

for line in sys.stdin:
  print(*line.split(' '), sep='\n', end='\n\n')
