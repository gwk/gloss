#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from argparse import ArgumentParser, FileType
from itertools import chain
from sys import stdin, stdout, stderr
from os import write

parser = ArgumentParser(description='Write lines of stdin to both stdout and stderr.')
parser.add_argument('-label', action='store_true',
  help="Prefix each line with 'out: ' and 'err: ' respectively.")
parser.add_argument('paths', type=FileType('rb'), nargs='*', default=[],
  help='Paths to read (similar to cat). Defaults to stdin.')

args = parser.parse_args()

label = args.label
inputs = args.paths or [stdin.buffer]
out = stdout.buffer
err = stderr.buffer

try:
  for line in chain.from_iterable(inputs):
    if label:
      out.write(b'out: ')
    out.write(line)
    out.flush()
    if label:
      err.write(b'err: ')
    err.write(line)
    err.flush()
except KeyboardInterrupt:
  exit('')
