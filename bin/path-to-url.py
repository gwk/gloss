#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import sys
import urllib.parse
import urllib.request


for line in sys.stdin:
  path = line.strip()
  print(urllib.parse.urljoin('file:', urllib.request.pathname2url(path)))

