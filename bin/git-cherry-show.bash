#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

git cherry "$1" "$2" | text-search -pattern '\+ (\w+)' -format '{0}' | xargs -L1 gsh
