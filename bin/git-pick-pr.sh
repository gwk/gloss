#!/bin/sh
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.


set -e

error() { echo "error:" "$@" 1>&2; exit 1; }
usage() { echo "usage: $0 [name] [commits...]" 1>&2;  exit 1; }

name="$1"; shift || usage
commits="$@"

echo "creating branch: $name..."
git branch "$name" --track upstream/master
git checkout "$name"

echo "picking commits: $commits..."
git cherry-pick $commits
git push origin $name
echo "done."
git checkout master
