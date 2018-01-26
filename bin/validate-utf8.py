#!/usr/bin/env python3
# Dedicated to the public dom  under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from sys import argv, stdin


def main():
  args = argv[1:]
  errors = False
  for path in args:
    with open(path, 'rb') as f:
      errors = check_file(f) and errors
  if not args:
    errors = check_file(stdin.buffer) and errors
  exit(1 if errors else 0)


def check_file(f) -> bool:
  errors = False
  for num, line_bytes in enumerate(f, 1):
    try: line_bytes.decode()
    except UnicodeError as e:
      print(f'{f.name}:{num}: error: {e}.\n  {line_bytes}')
      errors = True
  return errors


if __name__ == '__main__': main()
