# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# $@: The file name of the target of the rule.
# $<: The name of the first prerequisite.
# $^: The names of all the prerequisites, with spaces between them.
# $*: The matching string in a pattern rule.


.PHONY: _default build help install-vscode vscode vscode-keys vscode-keys-diff

# First target of a makefile is the default.
_default: help

build: _build/vscode/gloss-black.json _build/vscode/keybindings.json

help: # Summarize the targets of this makefile.
	@GREP_COLOR="1;32" egrep --color=always '^\w[^ :]+:' makefile | sort

install-vscode: vscode
	install/gloss-install-vscode.sh

vscode: _build/vscode/gloss-black.json _build/vscode/keybindings.json

vscode-keys: _build/vscode/keybindings.json

vscode-keys-diff: vscode
	d _build/vscode/keys-default.txt vscode/keys.txt


_build/vscode/gloss-black.json: gloss-black.py
	mkdir -p _build
	./$^ $@

_build/vscode/keybindings.json: vscode/keybindings.py vscode/keybindings-default.json vscode/keys.txt
	mkdir -p _build
	./$^ $@
