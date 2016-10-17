#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

[[ $# == 2 ]] || { echo "requires exactly two arguments (remote new-branch-name)." 1>&2; exit 1; };

git checkout -b "$2" && git push -u "$1" "$2"

