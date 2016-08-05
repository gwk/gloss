#!/usr/bin/env python3
# Copyright 2010 George King. Permission to use this file is granted in license-gloss.txt.

import sys
import locale

sys.exit(0 if locale.getpreferredencoding() == 'UTF-8' else 1)
