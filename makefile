# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# $@: The file name of the target of the rule.
# $<: The name of the first prerequisite.
# $^: The names of all the prerequisites, with spaces between them.
# $*: The matching string in a pattern rule.


.PHONY: _default build clean cov install-sys install-user install-vscode test uninstall-vscode

# First target of a makefile is the default.
_default: help

build: _build/gloss-black.json _build/vscode-keys.json

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

install-vscode: vscode
	install/gloss-install-vscode.sh

xcode_keys_src := keybindings/gloss-xcode.idebindings
xcode_keys_dst := ~/Library/Developer/Xcode/UserData/KeyBindings/gloss-xcode.idekeybindings
install-xcode-keybindings:
	[[ ! -f $(xcode_keys_dst) ]] || diff -u $(xcode_keys_src) $(xcode_keys_dst) || true
	cp -i $(xcode_keys_src) $(xcode_keys_dst)

test:
	iotest -fail-fast

uninstall-vscode:
	rm -rf ~/.vscode-insiders/extensions/gloss

vscode: _build/gloss-black.json _build/vscode-keys.json

vscode-keys-diff: vscode
	echo d _build/vscode-keys-defaults.txt vscode/vscode-keys.txt

_build/gloss-black.json: gloss-black.py
	mkdir -p _build
	./$^ $@

_build/vscode-keys.json: vscode/keybindings.py vscode/vscode-keys-default.json vscode/vscode-keys.txt
	./$^ $@
