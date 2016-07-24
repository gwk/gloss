#!/usr/bin/env bash

set -eux

VSCODE_GLOSS="$HOME/.vscode-insiders/extensions/gloss"
VSCODE_SYNTAXES="$VSCODE_GLOSS/syntaxes"
VSCODE_THEMES="$VSCODE_GLOSS/themes"
VSCODE_USER="$HOME/Library/Application Support/Code - Insiders/User"

rm -rf "$VSCODE_GLOSS"

mkdir -p \
"$VSCODE_GLOSS" \
"$VSCODE_SYNTAXES" \
"$VSCODE_THEMES" \
"$VSCODE_USER"

cp \
package.json \
swift-gloss.configuration.json \
"$VSCODE_GLOSS"

cp syntaxes/swift-gloss.json "$VSCODE_SYNTAXES"
cp _build/gloss-black.json "$VSCODE_THEMES"

cp _build/vscode-keys.json "$VSCODE_USER/keybindings.json"
