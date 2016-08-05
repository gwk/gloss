# Copyright 2014 George King. Permission to use this file is granted in license-gloss.txt.

target="$1"; shift
configuration="$1"; shift

[[ -z "$configuration" ]] && configuration="Release"

set -x
xcodebuild \
-target "$target" \
-configuration "$configuration" \
-showBuildSettings \
"$@"
