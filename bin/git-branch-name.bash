#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

git branch 2> /dev/null | grep '*' | cut -d ' ' -f 2

# alternative approach.
#branch=$(git symbolic-ref -q HEAD) # may be empty if detached.
#branch=${branch##refs/heads/} # remove refs/heads from front.
#branch=${branch:-HEAD} # if empty then HEAD.
