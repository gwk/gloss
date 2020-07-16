#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

set -eux

VSCODE_GLOSS="$HOME/.vscode-insiders/extensions/gloss"
VSCODE_THEMES="$VSCODE_GLOSS/themes"

craft-vscode-ext -name gloss -src vscode

# Not yet handled by craft-vscode-ext.
mkdir -p "$VSCODE_THEMES"
cp _build/vscode/gloss-black.json  "$VSCODE_THEMES"

# User settings.
VSCODE_USER="$HOME/Library/Application Support/Code - Insiders/User"
mkdir -p "$VSCODE_USER"
cp _build/vscode/keybindings.json  "$VSCODE_USER/keybindings.json"
