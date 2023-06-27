# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# $@: The file name of the target of the rule.
# $<: The name of the first prerequisite.
# $^: The names of all the prerequisites, with spaces between them.
# $*: The matching string in a pattern rule.


.PHONY: _default build clean cov install-sys install-user install-vscode keys test uninstall-vscode

# First target of a makefile is the default.
_default: help

build: _build/vscode/gloss-black.json _build/vscode/keybindings.json

clean:
	rm -rf _build/*

cov:
	iotest -fail-fast -coverage

help: # Summarize the targets of this makefile.
	@GREP_COLOR="1;32" egrep --color=always '^\w[^ :]+:' makefile | sort

install-sys:
	install/gloss-install-sys.py

install-user:
	install/gloss-install-user.py

install-dotfiles:
	install/gloss-install-dotfile-aliases.sh

install-vscode: vscode
	install/gloss-install-vscode.sh

keys: _build/vscode/keybindings.json

xcode_keys_src := keybindings/gloss-xcode.idebindings
xcode_keys_dst := ~/Library/Developer/Xcode/UserData/KeyBindings/gloss-xcode.idekeybindings
install-xcode-keybindings:
	[[ ! -f $(xcode_keys_dst) ]] || diff -u $(xcode_keys_src) $(xcode_keys_dst) || true
	cp -i $(xcode_keys_src) $(xcode_keys_dst)

py-deps:
	pip3 install keyring msgpack mypy-extensions toml twine typing-extensions zstandard

test:
	iotest -fail-fast

uninstall-vscode:
	rm -rf ~/.vscode{,-insiders}/extensions/gloss

vscode: _build/vscode/gloss-black.json _build/vscode/keybindings.json

vscode-keys-diff: vscode
	d _build/vscode/keys-default.txt vscode/keys.txt

_build/vscode/gloss-black.json: gloss-black.py
	mkdir -p _build
	./$^ $@

_build/vscode/keybindings.json: vscode/keybindings.py vscode/keybindings-default.json vscode/keys.txt
	mkdir -p _build
	./$^ $@
