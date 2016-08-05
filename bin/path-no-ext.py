#!/usr/bin/env python3
# Copyright 2010 George King. Permission to use this file is granted in license-gloss.txt.

# get the path minus the file extension

import sys
import os.path

if len(sys.argv) != 2:
  print('path_ext error: path_ext requires 1 argument', file=sys.stderr)
  sys.exit(1)

print(os.path.splitext(sys.argv[1])[0])
