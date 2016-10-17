# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# basic scripting utilities.

# ANSI select graphic rendition (SGR) control sequences.

export RST='\e[0m' # reset.
export RST_BOLD='\e[22m'
export RST_UNDERLINE='\e[24m'
export RST_BLINK='\e[25m'
export RST_INVERT='\e[27m'
export RST_TXT='\e[39m'
export RST_BG='\e[49m'

export BOLD='\e[1m'
export UNDERLINE='\e[4m'
export BLINK='\e[5m'
export INVERT='\e[7m'

export TXT_D='\e[30m' # dark gray
export TXT_R='\e[31m' # red
export TXT_G='\e[32m' # green
export TXT_Y='\e[33m' # yellow
export TXT_B='\e[34m' # blue
export TXT_M='\e[35m' # magenta
export TXT_C='\e[36m' # cyan
export TXT_L='\e[37m' # light gray

export BG_D='\e[40m' # dark gray
export BG_R='\e[41m' # red
export BG_G='\e[42m' # green
export BG_Y='\e[43m' # yellow
export BG_B='\e[44m' # blue
export BG_M='\e[45m' # magenta
export BG_C='\e[46m' # cyan
export BG_L='\e[47m' # light gray

# io.

out() { for i in "$@"; do printf "%s" "$i"; done; }; export -f out
outL() { out "$@"; printf "\n"; }; export -f outL
outS() { printf "%s" "$1"; shift; for i in "$@"; do printf " %s" "$i"; done; }; export -f outS
outSL() { outS "$@"; printf "\n"; }; export -f outSL
outLL() { for i in "$@"; do printf "%s\n" "$i"; done; }; export -f outLL
outF() { local format="$1"; shift; printf "$format" "$@"; }; export -f outF
outFL() { local format="$1\n"; shift; printf "$format" "$@"; }; export -f outFL

err()   { out    "$@" 1>&2; }; export -f err
errL()  { outL   "$@" 1>&2; }; export -f errL
errS()  { outS   "$@" 1>&2; }; export -f errS
errSL() { outSL  "$@" 1>&2; }; export -f errSL
errLL() { outLL  "$@" 1>&2; }; export -f errLL
errF()  { outF   "$@" 1>&2; }; export -f errF
errFL() { outFL  "$@" 1>&2; }; export -f errFL


# string functions.

# return true if $1 contains $2.
string_contains() { [[ "$1" != "${1/$2}" ]]; }; export -f string_contains

# return true if $1 has $2 as prefix.
string_has_prefix() { [[ "$1" != "${1##$2}" ]]; }; export -f string_has_prefix

# return true if $1 has $2 as suffix.
string_has_suffix() { [[ "$1" != "${1%%$2}" ]]; }; export -f string_has_suffix

# return true if none of the argument strings contain whitespace.
# test whether removing all spaces results in same string.
strings_contain_WS() { for s in "$@"; do [[ "$s" != "${s//[[:space:]]}" ]] && return 1; done; }; export -f strings_contain_WS

# shell mode detection functions.
is_shell_login()        { return $(shopt -q login_shell);   }; export -f is_shell_login
is_shell_interactive()  { return $([ -n "$PS1" ]);          }; export -f is_shell_interactive
is_shell_script()       { return $(! shell_is_interactive); }; export -f is_shell_script

prepend_gnu_to_path() { export PATH=/usr/local/gnu/bin:$PATH; export MANPATH=/usr/local/gnu/share/man:$MANPATH; }; export -f prepend_gnu_to_path;
