#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# cat text files, which will be decoded as utf8 one line at a time.
# files that contain invalid utf8 will cause exceptions.

import sys

def cat_file(bf):
  for i, line in enumerate(bf):
    try:
      text = line.decode('utf8')
      print(repr(text))
    except UnicodeDecodeError as e:
      print('!!INVALID-UTF8: ' + repr(line))


paths = sys.argv[1:]
if paths:
  for p in paths:
    with open(p, 'rb') as bf:
      cat_file(bf)
else:
  bf = sys.stdin.detach() # type: ignore [attr-defined] # get the underlying binary buffer.
  cat_file(bf)
