#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import sys


c = tuple(float(a) for a in sys.argv[1:4])

target_luminance = float(sys.argv[4])

input_luminance = .30 * c[0] + .59 * c[1] + .11 * c[2]

print('color:', c)
print('target luminance:', target_luminance)
print('input luminance:', input_luminance)



