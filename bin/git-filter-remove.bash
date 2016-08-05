#!/usr/bin/env bash
# Copyright 2013 George King. Permission to use this file is granted in license-gloss.txt.

# remove a file from a repository.

git filter-branch \
--index-filter "git rm -r --cached --ignore-unmatch '$@'" \
--prune-empty  \
--tag-name-filter cat -- \
--all
