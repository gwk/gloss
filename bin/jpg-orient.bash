#!/usr/bin/env bash
# Copyright 2010 George King. Permission to use this file is granted in license-gloss.txt.

# fix orientation tags losslessly using jhead


fail() { echo $*; exit 1; }

[[ -r "$1" ]] || fail "usage: jpg-orient [search_root]"

for i in $(find $1 -type f -name "*.jpg"); do
  echo "checking:" $i
  jhead -autorot $i || fail "jhead"
done
