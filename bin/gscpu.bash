#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

set -e

# Git switch create push upstream.

if [[ $# == 1 ]]; then
  remote="origin"
elif [[ $# == 2 ]]; then
  remote="$1"
  shift
else
  echo "gscpu requires one or two arguments (remote new-branch-name)." 1>&2
  exit 1
fi
branch="$1"

# Check if the branch already exists.
if git show-ref --verify --quiet refs/heads/"$branch"; then
  echo "Branch '$branch' already exists." 1>&2
  set -x
  git switch "$branch"
else
  # Create the new branch.
  set -x
  git switch -c "$branch"
fi

git push -u "$remote" "$branch"
