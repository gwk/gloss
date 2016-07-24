# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# $@: The file name of the target of the rule.
# $<: The name of the first prerequisite.
# $^: The names of all the prerequisites, with spaces between them. 


.PHONY: clean build install-sys install-user install-vscode uninstall-vscode

default: build

clean:
	rm -rf _build/*

build: _build/gloss-black.json _build/vscode-keys.json

install-sys:
	sudo install/gloss-install-sys.py

install-user:
	sudo install/gloss-install-user.py

install-vscode: _build/gloss-black.json _build/vscode-keys.json
	install/gloss-install-vscode.sh

uninstall-vscode:
	rm -rf ~/.vscode-insiders/extensions/gloss

_build/gloss-black.json: gloss-black.py
	./$^ $@

_build/vscode-keys.json: keybindings.py keys/vscode-keys-default.json keys/vscode-keys.txt
	./$^ $@
