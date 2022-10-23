#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

set -eux

VSCODE_USER="$HOME/Library/Application Support/Code/User"

mkdir -p "$VSCODE_USER"

# Diff the user settings and ask user if we should copy them into this repo.
set +x
touch "$VSCODE_USER/settings.json"
if ! d vscode/settings.json "$VSCODE_USER/settings.json"; then
  confirm 'format user settings and copy to this repo' \
  && json-fmt-in-place "$VSCODE_USER/settings.json" \
  && cp "$VSCODE_USER/settings.json"  vscode/settings.json \
  || echo "NOTE: user settings are not in sync with repo.
To format your settings: json-fmt-in-place vscode/settings.json
To overwrite your settings: cp vscode/settings.json '$VSCODE_USER/settings.json'"
fi
