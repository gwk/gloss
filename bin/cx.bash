#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

for path in "$@"; do
  if [[ -e "$path" ]]; then
    echo "file already exists: $path"
    continue
  else
    touch "$path" && chmod +x "$path"
  fi
done
