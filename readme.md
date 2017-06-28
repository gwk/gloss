# Gloss

Gloss is a set of enhancements to the Unix command line. It is primarily developed on macOS.


# Setup from scratch

A short guide to configuring your Mac.

## Prerequisites
Download and install the following:
* Latest Python 2 (https://python.org)
* Latest Python 3 (https://python.org)
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
* Fix up your PATH
  * TODO
...


# VSCode Development

* Press `F5` to launch a new instance of the editor with the extension loaded.
* If it does not work the first time then you may need to go to the debug mode (click the bug icon in the left toolbar of VSCode), and launch it with the GUI controls at the top of the pane.
* In the debug instance, select `File > Preferences > Color Themes` and pick `gloss-black`.
* Changes can be reloaded with `Cmd+R` from the debug instance.

