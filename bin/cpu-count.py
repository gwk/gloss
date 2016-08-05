#!/usr/bin/env python3
# Copyright 2010 George King. Permission to use this file is granted in license-gloss.txt.

# return the number of CPUs on the host machine, as determined by python.


import multiprocessing

print(multiprocessing.cpu_count())
