#!/usr/bin/env python3

from html import escape
from sys import argv


for arg in argv[1:]:
  print(escape(arg, quote=True))
