#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from argparse import ArgumentParser
from csv import reader
from sys import stderr


def main():
  parser = ArgumentParser(description='Read csv and output formatted columns.')
  parser.add_argument('-number-lines', action='store_true', help='prefix output with row number')
  parser.add_argument('-encoding', default='utf8', help='Text encoding used to read file.')
  parser.add_argument('-limit', type=int, help='limit output to specified number of rows')
  parser.add_argument('-format', help='A python format string to apply to each row.')
  parser.add_argument('-from', dest='from_', type=int, default=0, help='Row index to begin formatting.')
  parser.add_argument('-types', nargs='+', help='cast rows to the specified basic types: i/int, f/float, s/str')
  parser.add_argument('path', help='Path to CSV file.')
  args = parser.parse_args()

  if args.types:
    type_map = {
      'int'   : int,
      'float' : float,
      'str'   : str,
    }
    type_map.update((k[0], v) for k, v in list(type_map.items())) # add letter aliases.
    types = tuple(type_map[t] for t in args.types)
    def cast_row(row): return tuple(t(el) for t, el, in zip(types, row))
  else:
    def cast_row(row): return row

  for i, row in enumerate(reader(open(args.path, encoding=args.encoding))):
    try:
      if i < args.from_: continue
      if args.limit is not None and i >= args.limit:
        print('limit reached:', args.limit, file=stderr)
        break
      if args.number_lines:
        print('{:03}: '.format(i), end='')
      row = cast_row(row)
      if args.format:
        print(args.format.format(*row))
      else:
        print(*row)
    except:
      print('error: {}:{}:'.format(args.path, i))
      raise


if __name__ == '__main__': main()
