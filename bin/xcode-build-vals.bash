# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

target="$1"; shift
configuration="$1"; shift

[[ -z "$configuration" ]] && configuration="Release"

set -x
xcodebuild \
-target "$target" \
-configuration "$configuration" \
-showBuildSettings \
"$@"
