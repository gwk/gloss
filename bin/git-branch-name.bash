#!/usr/bin/env bash
# Copyright 2011 George King. Permission to use this file is granted in license-gloss.txt.

git branch 2> /dev/null | grep '*' | cut -d ' ' -f 2

# alternative approach.
#branch=$(git symbolic-ref -q HEAD) # may be empty if detached.
#branch=${branch##refs/heads/} # remove refs/heads from front.
#branch=${branch:-HEAD} # if empty then HEAD.
