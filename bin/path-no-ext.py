#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# get the path minus the file extension.

import sys
import os.path


if len(sys.argv) != 2:
  print('path_ext error: path_ext requires 1 argument', file=sys.stderr)
  sys.exit(1)

print(os.path.splitext(sys.argv[1])[0])
