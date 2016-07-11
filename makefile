# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# $@: The file name of the target of the rule.
# $<: The name of the first prerequisite.
# $^: The names of all the prerequisites, with spaces between them. 


.PHONY: clean build install uninstall

default: clean build install

clean:
	rm -f themes/gloss-black.json

build: themes/gloss-black.json

install_dir = ~/.vscode-insiders/extensions/gloss-black

install: build
	rm -rf $(install_dir)
	install -d $(install_dir)/syntaxes
	install -d $(install_dir)/themes
	install package.json $(install_dir)
	install swift-gloss.configuration.json $(install_dir)
	install syntaxes/swift-gloss.json $(install_dir)/syntaxes
	install themes/* $(install_dir)/themes

uninstall:
	rm -rf $(install_dir)

themes/gloss-black.json: gloss-black.py
	./$^ $@
