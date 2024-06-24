#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

'''
Generate random numeric strings.
'''

from secrets import randbelow
from random import randint, seed as seed_prng
from argparse import ArgumentParser, Namespace
from typing import Any


def main() -> None:
  parser = ArgumentParser(description=__doc__, add_help=False)

  parser.add_argument('-seed', type=int, help='The random seed.')
  parser.add_argument('-start', type=int, default=0, help='The start value (inclusive).')
  parser.add_argument('-hex', action='store_true', help='Output as hex.')
  parser.add_argument('-help', action='help', help='Show this help message and exit.')

  quantities = parser.add_mutually_exclusive_group(required=True)
  quantities.add_argument('-end', type=int, help='The end value (exclusive).')
  quantities.add_argument('-last', type=int, help='The last value (inclusive).')
  quantities.add_argument('-bits', type=int, help='The number of bits to generate.')
  quantities.add_argument('-bytes', type=int, help='The number of bytes to generate.')

  args = parser.parse_args()
  if seed := args.seed: seed_prng(seed)

  quantity_name, quantity = get_sole_arg(args, 'end', 'last', 'bits', 'bytes')

  start = args.start
  length = 0
  match quantity_name:
    case 'end':
      if quantity <= start: exit(f'Start value ({start}) must be less than end value ({quantity}).')
      length = quantity - start
    case 'last':
      if quantity < start: exit(f'Start value ({start}) must be less than or equal to last value ({quantity}).')
      length = start + quantity + 1
    case 'bits':
      if quantity < 0: exit(f'Bits value ({quantity}) must be non-negative.')
      length = (1 << quantity)
    case 'bytes':
      if quantity < 0: exit(f'Bytes value ({quantity}) must be non-negative.')
      length = (1 << (quantity * 8))
    case _: raise NotImplementedError(quantity_name)

  val = start + randbelow(length)
  if args.hex:
    print(hex(val))
  else:
    print(val)


def get_sole_arg(args: Namespace, *names:str) -> tuple[str, Any]:
  '''
  Verify that only a single one of the given arguments is specified, and return its name and value.
  If none or multiple of the arguments is specified, exit with an error message.
  '''
  sole_arg_name = None
  for name in names:
    if getattr(args, name) is None: continue
    if sole_arg_name is not None:
      exit(f'Only one of the following arguments may be specified: {", ".join(names)}')
    sole_arg_name = name
  if sole_arg_name is None:
    exit(f'One of the following arguments must be specified: {", ".join(names)}')
  return sole_arg_name, getattr(args, sole_arg_name)


if __name__ == '__main__': main()
