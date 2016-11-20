# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# $@: The file name of the target of the rule.
# $<: The name of the first prerequisite.
# $^: The names of all the prerequisites, with spaces between them.


.PHONY: _default build clean cov install-sys install-user install-vscode test uninstall-vscode

_default: build

# First target of a makefile is the default.
build: _build/gloss-black.json _build/vscode-keys.json

clean:
	rm -rf _build/*

cov:
	iotest -fail-fast -coverage

install-sys:
	sudo install/gloss-install-sys.py

install-user:
	sudo install/gloss-install-user.py

install-vscode: _build/gloss-black.json _build/vscode-keys.json
	install/gloss-install-vscode.sh

test:
	iotest -fail-fast

uninstall-vscode:
	rm -rf ~/.vscode-insiders/extensions/gloss

_build/gloss-black.json: gloss-black.py
	mkdir -p _build
	./$^ $@

_build/vscode-keys.json: keybindings.py keys/vscode-keys-default.json keys/vscode-keys.txt
	./$^ $@
