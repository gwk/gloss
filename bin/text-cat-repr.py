#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# Print text file line reprs, which will be decoded as utf8 one line at a time.
# Lines that contain invalid utf8 will print '!INVALID-UTF8:', the line number, and the repr of the bytes.

import sys
from typing import BinaryIO


def cat_file(bf:BinaryIO) -> None:
  for i, line in enumerate(bf, 1):
    try:
      text = line.decode('utf8')
      print(repr(text))
    except UnicodeDecodeError as e:
      print(f'!INVALID-UTF8:{i}:', repr(line))


paths = sys.argv[1:]
if paths:
  for p in paths:
    with open(p, 'rb') as bf:
      cat_file(bf)
else:
  bf = sys.stdin.detach() # type: ignore [union-attr] # get the underlying binary buffer.
  cat_file(bf)
