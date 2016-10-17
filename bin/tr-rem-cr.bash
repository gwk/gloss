#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# remove \r
# requires that tr recognize '\r' correctly.

error() { echo "error:" $*; exit 1; }

[[ $# -eq 2 ]] || error "usage: tr-rem-cr input_file output_file"
[[ "$1" != "$2" ]] || error "input and output files must differ"
[[ -r "$1" ]] || error "input is not readable: $1"
tr -d '\r' < "$1" > "$2"
