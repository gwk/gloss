#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# return the number of CPUs on the host machine, as determined by python.


import multiprocessing

print(multiprocessing.cpu_count())
