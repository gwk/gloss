#!/usr/bin/env bash
# Copyright 2011 George King. Permission to use this file is granted in license-gloss.txt.


for i in "$@"; do
  git diff --color=always ":2:$i" ":3:$i"
done
