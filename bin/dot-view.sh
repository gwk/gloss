#!/bin/sh
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

dot /dev/stdin -o /dev/stdout \
-Tsvg \
-Grankdir=LR -Gsplines=polyline \
-Gfontname=sans-serif -Nfontname=sans-serif -Efontname=sans-serif \
"$@" | html-view
