#!/usr/bin/env python
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

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
from sys import argv


var_name = argv[1]
argument_paths = argv[2:]

for i, p in enumerate(argument_paths, 2):
  if not p or ':' in p:
    exit('prepend-to-search-path: error: argument {} is empty or contains colon: {!r}'.format(i, p))

existing_var = environ.get(var_name)
# splitting empty string creates a single-element array of the empty string, which is bad.
existing_paths = existing_var.split(':') if existing_var else []

for p in existing_paths:
  if not p:
    exit('prepend-to-search-path: error: empty component in existing path\ninvocation: {}'.format(argv))

remaining_paths = [p for p in existing_paths if p not in argument_paths]
new_path = ':'.join(argument_paths + remaining_paths)
print(new_path)
