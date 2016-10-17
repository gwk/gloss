# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.


[[ $# == 1 ]] || { echo "$0 requires exactly one argument: the submodule ot remove." 1>&2; exit 1; }

git submodule deinit "$1"
git rm "$1"
