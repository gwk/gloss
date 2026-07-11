# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# Establish the gloss PATH and MANPATH ordering.
# This file is sourced by env.zsh for non-login shells, and by profile.zsh for login shells.
# The split exists because on macOS, /etc/zprofile runs after ~/.zshenv, and it invokes path_helper.
# `path_helper` reorders PATH and MANPATH to put /usr/bin first, in a way that we cannot control.
# login shells must therefore apply our desired ordering afterwards from ~/.zprofile.

# Keep entries unique. The first occurrence wins, so prepending an existing entry also promotes it.
typeset -U path PATH manpath MANPATH

# Prepend high-precedence directories, in decreasing precedence.
# The (N-/) glob qualifier drops any entry that is not an existing directory (following symlinks).
path=(
  /usr/local/bin(N-/) # From-source installs take precedence over homebrew.
  /opt/py/bin(N-/) # Custom python framework location.
  /opt/homebrew/bin(N-/)
  /opt/homebrew/sbin(N-/)
  $path
)

# Append low-precedence directories.
# Because typeset -U keeps only the first occurrence of a duplicate,
# appending a directory that is already present anywhere in $path has no effect;
# the entry would remain at its inherited position, possibly near the front.
# Therefore first delete any existing occurrence (${array:#pattern} filters matching elements), then append.
poth=(${path:#/opt/gloss/bin})
path=(${path:#$HOME/.local/bin})
path=(${path:#$HOME/.cargo/bin})
path+=(
  /opt/gloss/bin(N-/)
  ~/.local/bin(N-/) # `pip install --user` and similar per-user installs.
  ~/.cargo/bin(N-/) # Custom rustup/cargo location; see RUSTUP_HOME in env.zsh.
)

# Man pages for the custom installations above.
# Homebrew man pages are configured by `brew shellenv` in env.zsh; system defaults come from man itself.
manpath=(
  /opt/py/Python.framework/Versions/Current/share/man(N-/)
  /opt/rust/rustup/toolchains/*/share/man(N-/)
  $manpath
  '' # An empty final component (trailing colon) causes man to append its default search paths.
)
export MANPATH
