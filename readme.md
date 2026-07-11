# Gloss

Gloss is a set of enhancements to the Unix command line experience.
It consists of shell configurations and small utilities.
It currently targets modern macOS and Fedora Linux.


# Setup

## Prerequisites
* Python from source via `github.com/gwk/inish`.
* Pithy: `github.com/gwk/pithy`.

## Installation
* Run `sudo make install-sys` or `sudo install/gloss-install-sys.py`
* Run `make install-user` or `install/gloss-install-user.py`
* Run `make install-vscode` or `install/gloss-install-vscode.sh`
* Adjust your `.zprofile`, `.zshenv`, `.zshrc` as necessary.
* TODO: explain those adjustments in more detail.


# PATH configuration

Gloss establishes a consistent PATH ordering in `zsh/paths.zsh`.

macOS `/usr/libexec/path_helper` reorders PATH and MANPATH to force system paths first.
This happens after .zshenv but before .zprofile.
It first adds every line listed in `/etc/paths`, followed by every line listed in each file in `/etc/paths.d/*`,
and then appends any remaining preexisting entries.
`/etc/zprofile` sources `~/.zshenv` and `~/.zprofile` for login shells, after path_helper has run.
Therefore `/etc/paths.d` cannot express the desired ordering, so gloss does not use it.
Instead, `paths.zsh` is sourced from `env.zsh` (i.e. ~/.zshenv) for non-login shells,
and from `profile.zsh` (i.e. ~/.zprofile) for login shells, after path_helper has run.
Both cases source it exactly once, after any reordering, so all shells end up with the same PATH.

`gloss-install-sys.py` also writes /etc/sudoers.d/gloss-secure-path, setting the sudoers `secure_path`
to the same ordering restricted to root-owned, non-group/other-writable directories.
