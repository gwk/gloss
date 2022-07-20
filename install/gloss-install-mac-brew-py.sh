#!/usr/bin/env bash

fail() { echo $* 2>&1; exit 1; }

set -e

VERSION=3.10 # TODO: Make this version-independent.
VERSION_EXACT=3.10.5
if [[ $(uname) == 'Darwin' ]]; then
  echo 'Symlinking Python.app/Contents/MacOS/Python to python3.'
else
  fail 'This script currenly only works for macOS on Arm machines.'
fi

# Arm Mac Homebrew path.
FRAMEWORK=/opt/homebrew/Cellar/python@$VERSION/$VERSION_EXACT/Frameworks/Python.framework
FRAMEWORK_VERSION=$FRAMEWORK/Versions/$VERSION

[[ -d $FRAMEWORK ]] || fail 'ERROR: Python framework not found:' $FRAMEWORK
[[ -d $FRAMEWORK_VERSION ]] || fail 'ERROR: Python framework version directory not found:' $FRAMEWORK_VERSION

python_bin=$FRAMEWORK_VERSION/Resources/Python.app/Contents/MacOS/Python
#^ Link to the actual mac binary that gets executed, so that lldb can debug it.
# alternative: python_bin=$FRAMEWORK_VERSION/bin/python$VERSION

pip_bin=$FRAMEWORK_VERSION/bin/pip$VERSION

for suffix in '' '3' $VERSION; do
  ln -svf $python_bin /usr/local/bin/python$suffix
  ln -svf $pip_bin /usr/local/bin/pip$suffix
done
