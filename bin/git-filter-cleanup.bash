#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# cleanup after running a git filter-branch operation.

set -e

rm -rf .git/refs/original/

git reflog expire --expire=now --all

git gc --prune=now

# to be completely sure that a confidential object has been removed,
# gc should be run aggressively.
# git gc --aggressive --prune=now
