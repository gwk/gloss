#!/usr/bin/env python3
# Copyright 2014 George King. Permission to use this file is granted in license-gloss.txt.


import sys
import urllib.parse
import urllib.request

for line in sys.stdin:
  path = line.strip()
  print(urllib.parse.urljoin('file:', urllib.request.pathname2url(path)))

