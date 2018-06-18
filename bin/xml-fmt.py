#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# format xml from stdin to stdout.


from sys import argv, stdin

from xml.dom import minidom


if len(argv) == 1:
  f_in = stdin
else:
  f_in = open(argv[1])

if len(argv) > 2:
  exit('xml-fmt expects single argument: input path (defaults to stdin).')

xml = minidom.parse(f_in)
string = xml.toprettyxml(indent='  ')

for l in string.split('\n'):
  if not l.strip(): continue
  print(l)

