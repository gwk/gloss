#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# fix orientation tags losslessly using jhead


fail() { echo $* 2>&1; exit 1; }

[[ -r "$1" ]] || fail "usage: jpg-orient [search_root]"

for i in $(find $1 -type f -name "*.jpg"); do
  echo "checking:" $i
  jhead -autorot $i || fail "jhead"
done
