#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# requires that tr recognize '\r' correctly.
# replace \n with \r\n

error() { echo "error:" $*; exit 1; }

[[ $# -eq 2 ]] || error "usage: tr-to-lower input_file output_file"
[[ "$1" != "$2" ]] || error "input and output files must differ"
[[ -r "$1" ]] || error "input is not readable: $1"
tr '[:upper:]' '[:lower:]' < "$1" > "$2"
