#!/usr/bin/env bash

fail() { echo "error:" $* 2>&1; exit 1; }

set -e

FW_VERSIONED_PATH=$1
[[ -n "$FW_VERSIONED_PATH" ]] || fail "usage: $0 </opt/homebrew/Cellar/python@3.X/3.X/Frameworks/Python.framework/Versions/3.X>"
[[ -d "$FW_VERSIONED_PATH" ]] || fail "directory not found: $FW_VERSIONED_PATH"


if [[ $(uname) != 'Darwin' ]]; then
  fail 'This script currenly only works for macOS on Arm machines.'
fi

echo 'Symlinking Python.app/Contents/MacOS/Python to python3.'

python_bin=$FW_VERSIONED_PATH/Resources/Python.app/Contents/MacOS/Python
#^ Link to the actual mac binary that gets executed, so that lldb can debug it.
# alternative: python_bin=$FW_VERSIONED_PATH/bin/python$VERSION

pip_bin=$FW_VERSIONED_PATH/bin/pip$VERSION

for suffix in '' '3' $VERSION; do
  ln -svf $python_bin /usr/local/bin/python$suffix
  ln -svf $pip_bin /usr/local/bin/pip$suffix
done
