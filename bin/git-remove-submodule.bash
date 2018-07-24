# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.


[[ $# == 1 ]] || { echo "$0 requires exactly one argument: the submodule to remove." 1>&2; exit 1; }

set -e

git submodule deinit "$1"
git rm "$1"
echo 'run:'
echo '$ git commit'
echo "$ rm -rf .git/modules/$1"
