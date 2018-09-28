#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

set -eux

VSCODE_GLOSS="$HOME/.vscode-insiders/extensions/gloss"
VSCODE_THEMES="$VSCODE_GLOSS/themes"

craft-vscode-ext -name gloss -src vscode

# Not yet handled by craft-vscode-ext.
mkdir -p "$VSCODE_THEMES"
cp _build/gloss-black.json  "$VSCODE_THEMES"

# User settings.
VSCODE_USER="$HOME/Library/Application Support/Code - Insiders/User"
mkdir -p "$VSCODE_USER"
cp _build/vscode-keys.json  "$VSCODE_USER/keybindings.json"
set +x
touch "$VSCODE_USER/settings.json"
if ! d vscode/settings.json "$VSCODE_USER/settings.json"; then
  confirm 'copy user settings to this repo' \
  && cp "$VSCODE_USER/settings.json" vscode/settings.json \
  || echo "NOTE: user settings are not in sync with repo.
To overwrite your settings: cp vscode/settings.json '$VSCODE_USER/settings.json'"
fi
