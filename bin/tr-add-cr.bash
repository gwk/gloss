#!/usr/bin/env bash
# Copyright 2009 George King. Permission to use this file is granted in license-gloss.txt.

# requires that tr recognize '\r' correctly. 
# replace \n with \r\n

error() { echo "error:" $*; exit 1; }

[[ $# -eq 2 ]] || error "usage: tr-add-cr input_file output_file"
[[ "$1" != "$2" ]] || error "input and output files must differ"
[[ -r "$1" ]] || error "input is not readable: $1"
tr '\n' '\r\n' < "$1" > "$2"
