#!/usr/bin/env bash
# Copyright 2011 George King. Permission to use this file is granted in license-gloss.txt.


status=$(git status || exit 1)

count=$(echo $status | research -p "(\d+) commit")

[[ $? == 0 ]] || exit 1

git log --color-words -$count
