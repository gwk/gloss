#!/usr/bin/env bash
# Copyright 2013 George King. Permission to use this file is granted in license-gloss.txt.

# cleanup after running a git filter-branch operation.

set -e

rm -rf .git/refs/original/

git reflog expire --expire=now --all

git gc --prune=now

# to be completely sure that a confidential object has been removed,
# gc should be run aggressively.
# git gc --aggressive --prune=now
