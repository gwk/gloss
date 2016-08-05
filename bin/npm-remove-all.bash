set -o pipefail

npm ls -gp --depth=0 | awk -F/node_modules/ '{print $2}' | grep -vE '^npm$' | xargs npm -g rm
