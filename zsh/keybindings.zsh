# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

bindkey '^[[Z' reverse-menu-complete # Bind shift-tab to reverse-step through completion options.

bindkey -r '^J' # Unbind Ctrl-J, which defaults to redundant accept-line (same as Ctrl-M, which is also the Enter key).

stty discard undef # Disable tty output discard; Ctrl-O.
stty dsusp undef # Disable delayed suspend; Ctrl-Y.
stty kill undef # Disable tty kill-line; Ctrl-U.
stty lnext undef # Disable tty literal-next character; Ctrl-V.
stty quit undef # Disable SIGQUIT character; Ctrl-\.
stty reprint undef # Disable tty line reprint; Ctrl-R.
stty werase undef # Disable tty erase-word; Ctrl-W.

unsetopt FLOW_CONTROL # Disable software flow control (stop/XOFF, start/XON): frees Ctrl-S, Ctrl-Q.
