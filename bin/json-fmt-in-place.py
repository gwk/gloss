#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import sys
import json

from pithy.io import errFL


for path in sys.argv[1:]:
  try:
    with open(path) as f:
      o = json.load(f)
    with open(path, 'w') as f:
      json.dump(o, f, sort_keys=True, indent=2)
      f.write('\n')
  except Exception as e:
    io.errFL('exception: {}: {}', path, e)
