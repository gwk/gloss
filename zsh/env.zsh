
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

# Default to system-wide installation.
[[ -z "$GLOSS_DIR" ]] && export GLOSS_DIR=/usr/local/gloss
[[ -d "$GLOSS_DIR" ]] || errSL 'WARNING: bad GLOSS_DIR:' $GLOSS_DIR

# Calculate OS string.
_uname=$(uname)
if [[ $_uname == 'Darwin' ]]; then
  GLOSS_OS=mac
else
  GLOSS_OS=_uname
  errSL 'WARNING: unknown OS:' $GLOSS_OS
fi
export GLOSS_OS


case $GLOSS_OS in
  mac)
    export DISPLAY=:0 # MacPorts.
    PATHS=(
      /opt/homebrew/bin
      /opt/homebrew/sbin
      /usr/local/gloss/bin
      ~/.cargo/bin
    )
    #^ Place python directories after system directories for safety;
    # we do not want pip-installed executables to mask system ones.
    # Note that python and its other core executables are symlinked to /usr/local/bin.
    ;;
  *)
    echo "WARNING: PATH not configured for unknown OS; $GLOSS_OS"
    ;;
esac

# Apple's /usr/libexec/path_helper enforces a basic PATH ordering.
# This is everything listed in /etc/paths, followed by everything listed in /etc/paths.d/*.
# path_helper is called in /etc/zprofile, which is sourced after ~/.zshenv (which sources this file).
export PATH="${(j[:])PATHS}" # Join the paths with colons.
export PAGER=less

case $GLOSS_OS in
  mac)
    EDITOR='code -w "$@"' # Use VS Code as the shell editor.
esac
export EDITOR


export HELPDIR=/usr/share/zsh/5.8/help

# Standard homebrew configuration.
export HOMEBREW_PREFIX="/opt/homebrew";
export HOMEBREW_CELLAR="/opt/homebrew/Cellar";
export HOMEBREW_REPOSITORY="/opt/homebrew";
export MANPATH="/opt/homebrew/share/man${MANPATH+:$MANPATH}:";
export INFOPATH="/opt/homebrew/share/info:${INFOPATH:-}";


# ANSI select graphic rendition (SGR) control sequences.
# $'' form causes the shell to parse ANSI C escapes.
export RST=$'\e[0m' # Reset.
export RST_BOLD=$'\e[22m'
export RST_ULINE=$'\e[24m'
export RST_BLINK=$'\e[25m'
export RST_INVERT=$'\e[27m'
export RST_TXT=$'\e[39m'
export RST_BG=$'\e[49m'

export BOLD=$'\e[1m'
export ULINE=$'\e[4m'
export BLINK=$'\e[5m'
export INVERT=$'\e[7m'

export TXT_K=$'\e[30m' # Black.
export TXT_R=$'\e[31m' # Red.
export TXT_G=$'\e[32m' # Green.
export TXT_Y=$'\e[33m' # Yellow.
export TXT_B=$'\e[34m' # Blue.
export TXT_M=$'\e[35m' # Magenta.
export TXT_C=$'\e[36m' # Cyan.
export TXT_W=$'\e[37m' # White.

export BG_K=$'\e[40m' # Black.
export BG_R=$'\e[41m' # Red.
export BG_G=$'\e[42m' # Green.
export BG_Y=$'\e[43m' # Yellow.
export BG_B=$'\e[44m' # Blue.
export BG_M=$'\e[45m' # Magenta.
export BG_C=$'\e[46m' # Cyan.
export BG_W=$'\e[47m' # White.
