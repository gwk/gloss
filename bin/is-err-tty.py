#!/usr/bin/env python3
# Copyright 2010 George King. Permission to use this file is granted in license-gloss.txt.

from sys import stderr

exit(0 if stderr.isatty() else 1)
