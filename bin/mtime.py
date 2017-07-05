#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from datetime import datetime
from os import stat
from sys import argv


if len(argv) < 2: exit('usage: mtime [paths...]')

ok = True
for path in argv[1:]:
  try: mtime = stat(path).st_mtime
  except FileNotFoundError:
    ok = False
    print(f'{path}: no such file or directory')
    continue
  print(f'{path}: {datetime.fromtimestamp(mtime)} ({mtime})')

exit(0 if ok else 1)
