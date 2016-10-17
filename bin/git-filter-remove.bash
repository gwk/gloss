#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# remove a file from a repository.

git filter-branch \
--index-filter "git rm -r --cached --ignore-unmatch '$@'" \
--prune-empty  \
--tag-name-filter cat -- \
--all
