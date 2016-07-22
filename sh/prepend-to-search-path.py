#!/usr/bin/env python
# Copyright 2011-2016 George King. Permission to use this file is granted in license-gloss.txt.

'''
Print a colon delimited search path string.
The first argument is the name of the environment variable, e.g. PATH or PYTHONPATH.
The remaining arguments are the paths to prepend to the existing value.
Note: this is a python2 script so that we can set up the PATH,
which might not yet contain python3; python2 is more likely to be be installed on the system.

Note: the script must not create a search path with leading or trailing colons,
or an empty element indicated by '::', as these will be interpreted as '/'.
'''

from __future__ import print_function

from os import environ
from sys import argv, stderr


var_name = argv[1]
argument_paths = argv[2:]

for p in argument_paths:
  if not p or ':' in p:
    print('prepend-to-search-path: error: argument is empty or contains colon:', repr(p), file=stderr)
    print('invocation:', argv, file=stderr)
    exit(1)

existing_var = environ.get(var_name)
# splitting empty string creates a single-element array of the empty string, which is bad.
existing_paths = existing_var.split(':') if existing_var else []

for p in existing_paths:
  if not p:
    print('prepend-to-search-path: error: empty component in existing path', file=stderr)
    print('invocation:', argv, file=stderr)
    exit(1)

remaining_paths = [p for p in existing_paths if p not in argument_paths]
new_path = ':'.join(argument_paths + remaining_paths)
print(new_path)
