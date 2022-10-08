#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import re
from argparse import ArgumentParser
from typing import Any, Callable


def main() -> None:
  parser = ArgumentParser(description='Parse and print color channel values in a variety of representations.')
  parser.add_argument('-decimal',      action='store_true', help='8 bit decimal values (0-255)')
  parser.add_argument('-hexadecimal',  action='store_true', help='8 bit hexadecimal values (00-FF')
  parser.add_argument('-normal',       action='store_true', help='normalized decimal values (0-1)')
  parser.add_argument('components', nargs='+', help='color components to convert')
  args = parser.parse_args()

  pattern = r'\d+(?:\.\d*)?|\.\d+' # decimal parser
  type_fn:Callable[[str],float] = float

  if args.normal:
    scale = 1
  elif args.decimal:
    scale = 255
  elif args.hexadecimal:
    pattern =r'(?:0x)?[0-9a-fA-F]{2}'
    type_fn = lambda x: int(x, 16)
    scale = 255
  else:
    exit('error: no mode flag set; specify one of: -decimal, -hexadecimal, or -normal.')

  r = re.compile(pattern)

  # Do away with any non-numeric cruft or shell word-splitting by joining all component args and then scanning.
  s = ' '.join(args.components)
  components = [min(1.0, (type_fn(x) / scale)) for x in r.findall(s)]

  while len(components) < 3:
    components.append(0.0)
  while len(components) < 4:
    components.append(1.0)

  components_scaled = [int(round(c * 255)) for c in components]

  for l, c in zip('rgba', components):
    outZ(f'{l}:{c:.3f} ')

  outZ('   ({})'.format(', '.join('{:.3f}'.format(c) for c in components)))

  outZ('    hex: #')
  for i, c in enumerate(components_scaled):
    if i > 2: outZ(' ')
    outZ(f'{c:02X}')

  outZ('    dec:')
  for c in components_scaled:
    outZ(f' {c:03}')

  print()


def outZ(*items:Any) -> None: print(*items, end='')


main()
