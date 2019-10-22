#!/bin/bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# Split leading positional args from trailing option args in $@.
inputs=""
while [[ -n "$@" ]]; do
  if [[ "$1" == -* ]]; then
    break
  else
    inputs="$args $1"
    shift
  fi
done

if [[ -n "$args" ]]; then
  inputs=/dev/stdin
fi

dot $inputs -o /dev/stdout \
-Tsvg \
-Grankdir=LR -Gsplines=polyline \
-Gfontname=sans-serif -Nfontname=sans-serif -Efontname=sans-serif \
-Ecolor="#606060" \
"$@" | html-view
