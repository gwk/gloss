#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.


for i in "$@"; do
  git diff ":2:$i" ":3:$i"
done
