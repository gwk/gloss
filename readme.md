# Gloss

Gloss is a set of enhancements to the Unix command line experience.
It consists of shell configurations and small utilities.
It is primarily developed on macOS but is also actively used with Amazon Linux 2022.


# Setup

## Prerequisites
Download and install the following:
* Latest Python 3 (For Mac, download from https://python.org or install via Homebrew)
* Optional: Visual Studio Code (https://code.visualstudio.com)

## Installation
* Run the Python installers.
* If you would like to use VSCode, download it and drag the application to your system Applications folder.
* Install the `code` command line shortcut for VSCode:
  * Open VSCode
  * From the View menu select `Command Palette...`
  * In the command field, type "Shell command: Install 'code' command in PATH command" (it should autocomplete after a few characters)
  * Hit return to run the command; this will create a symlink from `/usr/local/bin/code` to the program inside the application bundle.
  * You can now use the `code` command in the console to open files and folders.
* Run `sudo make install-sys` or `sudo install/gloss-install-sys.py`
* Run `make install-user` or `install/gloss-install-user.py`
* Run `make install-vscode` or `install/gloss-install-vscode.sh`
* Adjust your `.zprofile`, `.zshenv`, `.zshrc` as necessary.
* TODO: explain those adjustments in more detail.


# VSCode Development

* Press `F5` to launch a new instance of the editor with the extension loaded.
* If it does not work the first time then you may need to go to the debug mode (click the bug icon in the left toolbar of VSCode), and launch it with the GUI controls at the top of the pane.
* In the debug instance, select `File > Preferences > Color Themes` and pick `gloss-black`.
* Changes can be reloaded with `Cmd+R` from the debug instance.


# PATH configuration

Gloss establishes a consistent PATH ordering in `zsh/paths.zsh`.

Apple's `/usr/libexec/path_helper` reorders PATH and MANPATH to force system paths first.
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
