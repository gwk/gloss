#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# print the last word of the last argument.


from sys import argv

if len(argv) < 2:
  exit('last_word error: no arguments')

print(argv[-1].split()[-1])
