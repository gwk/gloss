#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

set -e

if [[ $# == 1 ]]; then
  remote="origin"
elif [[ $# == 2 ]]; then
  remote="$1"
  shift
else
  echo "requires one or two arguments (remote new-branch-name)." 1>&2
  exit 1
fi
branch="$1"

# Check if the branch already exists.
if git show-ref --verify --quiet refs/heads/"$branch"; then
  echo "Branch '$branch' already exists." 1>&2
  git checkout "$branch"
else
  # Create the new branch.
  git checkout -b "$branch"
fi

git push -u "$remote" "$branch"
