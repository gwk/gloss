#!/usr/bin/env python3
# Copyright 2010 George King. Permission to use this file is granted in license-gloss.txt.

from sys import stdout

exit(0 if stdout.isatty() else 1)
