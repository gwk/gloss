#!/usr/bin/env bash
# Copyright 2014 George King. Permission to use this file is granted in license-gloss.txt.

[[ $# == 2 ]] || { echo "requires exactly two arguments (remote new-branch-name)." 1>&2; exit 1; };

git checkout -b "$2" && git push -u "$1" "$2"

