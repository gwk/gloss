#!/usr/bin/env bash
# Copyright 2014 George King. Permission to use this file is granted in license-gloss.txt.

# strip resource forks from files.

for p in $@; do
  cat /dev/null > "$p/..namedfork/rsrc"
  SetFile -a c "$p" # remove custom icon
done
