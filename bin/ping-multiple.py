#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# ping multiple hosts simultaneously.

import sys
import subprocess
import time


if (len(sys.argv) < 2):
  sys.exit("specify a list of hosts to ping")

hosts = sys.argv[1:]

for host in hosts:
  cmd = ("ping", host)
  print(cmd)
  sp = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr, close_fds=True)

try:
  while True:
    print("----")
    time.sleep(1)
except KeyboardInterrupt:
  sys.exit(0)
