#!/usr/bin/env bash
# Copyright 2012 George King. Permission to use this file is granted in license-gloss.txt.


set -e

# filter out commented lines with grep
urls=$(egrep -v '^#' "$@")

for url in $urls; do
  echo $url
  curl -O $url
done
