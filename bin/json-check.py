#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from sys import argv
from json import JSONDecoder
from typing import Any


def object_pairs_hook(pairs:list[tuple[str,Any]]) -> dict[str,Any]:
  keys = set()
  for k, v in pairs:
    if k in keys:
      print('DUPLICATE KEY:', k, ':', v,'\n')
    else:
      keys.add(k)
  return dict(pairs)

decoder = JSONDecoder(object_pairs_hook=object_pairs_hook)

for path in argv[1:]:
  try:
    string = open(path).read()
  except Exception as e:
    print('error: {}: {}'.format(path, e))
    continue
  try:
    decoder.decode(string)
  except Exception as e:
    print('error: {}: {}'.format(path, e))

