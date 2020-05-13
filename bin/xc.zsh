#!/usr/bin/env zsh

beta_suffix=""
if [[ "$1" == "-beta" ]]; then
  beta_suffix="-Beta"
  shift
fi

setopt NULL_GLOB
args=($@)
[[ "$args" ]] || args=(*.xcworkspace)
[[ "$args" ]] || args=(*.xcodeproj)

open -a Xcode$beta_suffix "$args"
