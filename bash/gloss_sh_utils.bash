# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# basic scripting utilities.

# io.

out() { for i in "$@"; do printf "%s" "$i"; done; };
outL() { out "$@"; printf "\n"; };
outS() { printf "%s" "$1"; shift; for i in "$@"; do printf " %s" "$i"; done; };
outSL() { outS "$@"; printf "\n"; };
outLL() { for i in "$@"; do printf "%s\n" "$i"; done; };
outF() { local format="$1"; shift; printf "$format" "$@"; };
outFL() { local format="$1\n"; shift; printf "$format" "$@"; };

err()   { out    "$@" 1>&2; };
errL()  { outL   "$@" 1>&2; };
errS()  { outS   "$@" 1>&2; };
errSL() { outSL  "$@" 1>&2; };
errLL() { outLL  "$@" 1>&2; };
errF()  { outF   "$@" 1>&2; };
errFL() { outFL  "$@" 1>&2; };


# string functions.

# return true if $1 contains $2.
string_contains() { [[ "$1" != "${1/$2}" ]]; };

# return true if $1 has $2 as prefix.
string_has_prefix() { [[ "$1" != "${1##$2}" ]]; };

# return true if $1 has $2 as suffix.
string_has_suffix() { [[ "$1" != "${1%%$2}" ]]; };

# return true if none of the argument strings contain whitespace.
# test whether removing all spaces results in same string.
strings_contain_WS() { for s in "$@"; do [[ "$s" != "${s//[[:space:]]}" ]] && return 1; done; };

# shell mode detection functions.
is_shell_login()        { return $(shopt -q login_shell);   };
is_shell_interactive()  { return $([ -n "$PS1" ]);          };
is_shell_script()       { return $(! shell_is_interactive); };

prepend_gnu_to_path() { export PATH=/usr/local/gnu/bin:$PATH; export MANPATH=/usr/local/gnu/share/man:$MANPATH; };
