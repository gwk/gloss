#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# return the number of CPUs on the host machine, as determined by python.


from multiprocessing import cpu_count

print(cpu_count())
