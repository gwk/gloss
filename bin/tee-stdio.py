#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from sys import stdin, stdout, stderr
from argparse import ArgumentParser


parser = ArgumentParser(description='Write lines of stdin to both stdout and stderr.')
parser.add_argument('-label', action='store_true', help="Prefix each line with 'out: ' and 'err: ' respectively.")
args = parser.parse_args()

label = args.label

for line in stdin:
  if label:
    stdout.write('out: ')
  stdout.write(line)
  if label:
    stderr.write('err: ')
  stderr.write(line)
