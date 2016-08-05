#!/usr/bin/env bash
# Copyright 2009 George King. Permission to use this file is granted in license-gloss.txt.

# remove \r
# requires that tr recognize '\r' correctly. 

error() { echo "error:" $*; exit 1; }

[[ $# -eq 2 ]] || error "usage: tr-rem-cr input_file output_file"
[[ "$1" != "$2" ]] || error "input and output files must differ"
[[ -r "$1" ]] || error "input is not readable: $1"
tr -d '\r' < "$1" > "$2"
