#!/usr/bin/env bash
# Copyright 2014 George King. Permission to use this file is granted in license-gloss.txt.

for path in "$@"; do
  if [[ -e "$path" ]]; then
    echo "file already exists: $path"
    continue
  else
    touch "$path" && chmod +x "$path"
  fi
done
