# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# .zshenv is loaded every time, prior to zprofile or zshrc.
# Source this file from your .zshenv with the following command:
#   source /usr/local/gloss/zsh/env.zsh

export GLOSS_ENV=GLOSS_ENV

# Printing functions.
out()   { print -n - ${(j..)@} }
outL()  { print - ${(j..)@} }
outS()  { print -n - $@ }
outSL() { print - $@ }
outLL() { print -l - $@ }
outF()  { printf -n - $@ }
outFL() { printf - $@ }

err()   { >&2 print -n - ${(j..)@} }
errL()  { >&2 print - ${(j..)@} }
errS()  { >&2 print -n - $@ }
errSL() { >&2 print - $@ }
errLL() { >&2 print -l - $@ }
errF()  { >&2 printf -n - $@ }
errFL() { >&2 printf - $@ }

# Source gloss custom environment if it exists.
[[ -f ~/.config/gloss.env ]] && source ~/.config/gloss.env

# Default to system-wide installation.
[[ -z "$GLOSS_DIR" ]] && export GLOSS_DIR=/usr/local/gloss
[[ -d "$GLOSS_DIR" ]] || errSL 'WARNING: bad GLOSS_DIR:' $GLOSS_DIR

[[ -n "$PATH" ]] || errSL 'WARNING: PATH is empty when gloss env.zsh is sourced.'
export PATH="$PATH:$GLOSS_DIR/bin"

# Get gloss platform string.
export GLOSS_OS=$(cut -f1 $GLOSS_DIR/platform.txt)
export GLOSS_DISTRO=$(cut -f2 $GLOSS_DIR/platform.txt)

export PAGER=less
export HELPDIR=/usr/share/zsh/5.8/help

case $GLOSS_OS in
  linux)
    export EDITOR=nano;;
  mac)
    export EDITOR='code -w "$@"' # Use VS Code as the shell editor.
    # Standard homebrew configuration.
    export HOMEBREW_PREFIX="/opt/homebrew"
    export HOMEBREW_CELLAR="/opt/homebrew/Cellar"
    export HOMEBREW_REPOSITORY="/opt/homebrew"
    export MANPATH="/opt/homebrew/share/man${MANPATH+:$MANPATH}:"
    export INFOPATH="/opt/homebrew/share/info:${INFOPATH:-}";;
esac


# ANSI select graphic rendition (SGR) control sequences.
# $'' form causes the shell to parse ANSI C escapes.
# Note: the resets are ordered after the codes so that `env` looks less crazy.

export BOLD=$'\e[1m'
export RST_BOLD=$'\e[22m'
export ULINE=$'\e[4m'
export RST_ULINE=$'\e[24m'
export BLINK=$'\e[5m'
export RST_BLINK=$'\e[25m'
export INVERT=$'\e[7m'
export RST_INVERT=$'\e[27m'

export TXT_K=$'\e[30m' # Black.
export TXT_R=$'\e[31m' # Red.
export TXT_G=$'\e[32m' # Green.
export TXT_Y=$'\e[33m' # Yellow.
export TXT_B=$'\e[34m' # Blue.
export TXT_M=$'\e[35m' # Magenta.
export TXT_C=$'\e[36m' # Cyan.
export TXT_W=$'\e[37m' # White.
export RST_TXT=$'\e[39m'

export BG_K=$'\e[40m' # Black.
export BG_R=$'\e[41m' # Red.
export BG_G=$'\e[42m' # Green.
export BG_Y=$'\e[43m' # Yellow.
export BG_B=$'\e[44m' # Blue.
export BG_M=$'\e[45m' # Magenta.
export BG_C=$'\e[46m' # Cyan.
export BG_W=$'\e[47m' # White.
export RST_BG=$'\e[49m'

export RST=$'\e[0m' # Reset everything.
