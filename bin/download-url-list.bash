#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.


set -e

# filter out commented lines with grep
urls=$(egrep -v '^#' "$@")

for url in $urls; do
  echo $url
  curl -O $url
done
