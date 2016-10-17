#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# strip resource forks from files.

for p in $@; do
  cat /dev/null > "$p/..namedfork/rsrc"
  SetFile -a c "$p" # remove custom icon
done
