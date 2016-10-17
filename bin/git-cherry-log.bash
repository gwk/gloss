#!/usr/bin/env bash
# Copyright 2011 George King. Permission to use this file is granted in license-gloss.txt.

git cherry "$1" "$2" | text-search -pattern '\+ (\w+)' -format '{0}' | xargs -L1 gl1
