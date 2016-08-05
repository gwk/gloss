#!/usr/bin/env python3
# Copyright 2013 George King. Permission to use this file is granted in license-gloss.txt.

import sys

for line in sys.stdin:
  print(*line.split(' '), sep='\n', end='\n\n')
