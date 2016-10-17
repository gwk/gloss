#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.


status=$(git status || exit 1)

count=$(echo $status | research -p "(\d+) commit")

[[ $? == 0 ]] || exit 1

git log --color-words -$count
