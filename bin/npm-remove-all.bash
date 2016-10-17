# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

set -o pipefail

npm ls -gp --depth=0 | awk -F/node_modules/ '{print $2}' | grep -vE '^npm$' | xargs npm -g rm
