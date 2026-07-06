# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# Format the Zed default keymap after it has been pasted into zed/keymap-default.jsonc
# (obtained via the "zed: open default keymap" command palette action).
zed-keymap:
	json-fmt-in-place -fix -comments zed/keymap-default.jsonc zed/keymap.jsonc
	python zed/keymap.py zed/keymap-default.jsonc zed/keymap.jsonc
