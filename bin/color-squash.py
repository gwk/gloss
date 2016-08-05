#!/usr/bin/env python3
# Copyright 2011 George King. Permission to use this file is granted in license-gloss.txt.

import sys

c = tuple(float(a) for a in sys.argv[1:4])

target_luminance = float(sys.argv[4])

input_luminance = .30 * c[0] + .59 * c[1] + .11 * c[2]

print('color:', c)
print('target luminance:', target_luminance)
print('input luminance:', input_luminance)



