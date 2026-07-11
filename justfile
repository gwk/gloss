# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.


# List all recipes; the default.
list-recipes:
  @just --list --unsorted

link-claude-md:
  find . -name 'AGENTS.md' -print0 | xargs -0 -I {} sh -c 'ln -sf "$(basename {})" "$(dirname {})/CLAUDE.md"'


# Format the Zed default keymap after it has been pasted into zed/keymap-default.jsonc
# (obtained via the "zed: open default keymap" command palette action).
zed-keymap:
  json-fmt-in-place -fix -comments zed/keymap-default.jsonc zed/keymap.jsonc
  python zed/keymap.py zed/keymap-default.jsonc zed/keymap.jsonc


# Remove all build products.
clean:
  rm -rf _build/*

# Run tests with coverage.
cov:
  iotest -fail-fast -coverage

# Run tests.
test:
  iotest -fail-fast

# Typecheck with mypy.
typecheck:
  mypy .

# Install the system configuration.
install-sys:
  sudo install/gloss-install-sys.py

# Install the user configuration.
install-user:
  install/gloss-install-user.py

# Install the dotfile aliases.
install-dotfiles:
  install/gloss-install-dotfile-aliases.sh

xcode_keys_src := "keybindings/gloss-xcode.idebindings"
xcode_keys_dst := "~/Library/Developer/Xcode/UserData/KeyBindings/gloss-xcode.idekeybindings"

# Install the Xcode keybindings.
install-xcode-keybindings:
  [[ ! -f {{xcode_keys_dst}} ]] || diff -u {{xcode_keys_src}} {{xcode_keys_dst}} || true
  cp -i {{xcode_keys_src}} {{xcode_keys_dst}}

# Uninstall the VSCode extension.
uninstall-vscode:
  rm -rf ~/.vscode/extensions/gloss

# Install the Python dependencies.
py-deps:
  pip3 install keyring msgpack mypy-extensions toml twine typing-extensions zstandard
