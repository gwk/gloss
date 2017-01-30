#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

set -eux

VSCODE_GLOSS="$HOME/.vscode-insiders/extensions/gloss"
VSCODE_CONFIGURATIONS="$VSCODE_GLOSS/configurations"
VSCODE_SYNTAXES="$VSCODE_GLOSS/syntaxes"
VSCODE_THEMES="$VSCODE_GLOSS/themes"
VSCODE_USER="$HOME/Library/Application Support/Code - Insiders/User"

rm -rf "$VSCODE_GLOSS"/*

mkdir -p \
"$VSCODE_GLOSS" \
"$VSCODE_CONFIGURATIONS" \
"$VSCODE_SYNTAXES" \
"$VSCODE_THEMES" \
"$VSCODE_USER"

cp \
package.json \
"$VSCODE_GLOSS"

cp configurations/*.json    "$VSCODE_CONFIGURATIONS"
cp syntaxes/*.json          "$VSCODE_SYNTAXES"
cp _build/gloss-black.json  "$VSCODE_THEMES"

cp _build/vscode-keys.json "$VSCODE_USER/keybindings.json"
