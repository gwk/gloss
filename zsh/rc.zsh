# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# .zshrc is sourced for interactive shells.
# Source this file from your .zshrc with the following command:
#   source /opt/gloss/zsh/rc.zsh

# Various zsh options.

source $GLOSS_DIR/zsh/keybindings.zsh

setopt interactive_comments # Allows typing or pasting a comment into the interactive shell.
setopt noclobber # Do not allow file overwrites with regular io redirects.
setopt pipefail # Pipe failures cause processes to signal/terminate.

setopt HIST_FIND_NO_DUPS # Do not display duplicates of a line previously found, even if the duplicates are not contiguous.
#setopt HIST_IGNORE_ALL_DUPS # A new history list command causes older duplicates to be removed from the list (even if not contiguous).
#setopt HIST_IGNORE_DUPS # Do not enter command lines into the history list if they are duplicates of the previous event.

setopt HIST_IGNORE_DUPS # Do not enter command lines into the history list if they are duplicates of the previous event.

# These are set by default on macOS but not on Linux.
export HISTFILE=~/.zsh_history
export HISTSIZE=2000
export SAVEHIST=1000

setopt SHARE_HISTORY # Write to the history file immediately, not when the shell exits.
#^ Do not also set INC_APPEND_HISTORY. See: https://zsh.sourceforge.io/Doc/Release/Options.html#History.

setopt AUTO_LIST # List choices on ambiguous completion.
setopt AUTO_MENU # Use menu completion on double-tab.
setopt AUTO_PARAM_KEYS # Automatically added spaces will be removed for syntactic closing characters that follow.
setopt AUTO_PARAM_SLASH # Add trailing slash instead of space for directory names.
setopt IGNORE_EOF # Prevent ctrl-d from closing the shell (and terminal window).
#setopt LIST_AMBIGUOUS # Auto-listing only takes place when nothing would be inserted.
setopt LIST_PACKED # Use more compact, variable-width columns.
setopt LIST_TYPES

zmodload zsh/nearcolor # Approximate 24 bit color as necessary.

# Enable run-help.
unalias run-help
autoload run-help

# Disable paste highlighting.
export zle_highlight=(region:standout special:standout suffix:bold isearch:underline paste:none)

# zsh completion system.
zstyle ':completion:*' menu select
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}'

# Homebrew completion.
if [[ -n "${HOMEBREW_PREFIX-}" ]]; then
  fpath=($HOMEBREW_PREFIX/share/zsh/site-functions $fpath)
fi

# Personal functions and completions; these come after Homebrew to allow for overrides.
fpath=(~/.zfunc $fpath)

# Listing colors are controlled by the complist module's `list-colors` zstyle, which matches display strings.
# The `(#b)` activates backreferences; the first `=0` styles the whole match and `=2` (faint) styles the group.
zstyle ':completion:*' group-name '' # List each group separately instead of merging.
zstyle ':completion:*:descriptions' format '%B%F{8}# %d%f%b'  # Bold gray heading; 8 is "bright black". Try 242 for mid-gray.
zstyle ':completion:*:commands' list-colors '=(#b)([^ ]##)( : *)=0=33=2' '=*=33'  # Yellow names, dim descriptions.
zstyle ':completion:*:options'  list-colors '=(#b)([^ ]##)( : *)=0=36=2' '=*=36'  # Cyan flags, dim descriptions.

# Do not run compinit here; users may extend fpath after sourcing this file.

# Environment variables for various other tools.

export COLORTERM=truecolor

export LESS=FRX
export CLICOLOR=1 # Enable colors in ls.

export GREP_OPTIONS="--color=auto --binary-files=without-match"
export GREP_COLOR='4' # Highlight matches with underline. macOS only recognizes the old var.
export GREP_COLORS='mt=4' # Highlight matches with underline. Linux wants the new var or else complains about deprecation.

export NODE_REPL_MODE=strict


# Utility functions.

# List all aliases/functions defined in this shell environment.
# These are stored in associative arrays; -k gives us keys only; -o sorts.
list-aliases() { print -c ${(ko)aliases} }
list-functions() { print -c ${(ko)functions} }


# Command prompt customization.

# The user can override these at any time.
export GLOSS_PROMPT_SYMBOL='❯' # Heavy Right-Pointing Angle Quotation Mark Ornament.
export GLOSS_PROMPT_SSH_SYMBOL='§'
export GLOSS_PROMPT_PREFIX_STYLE=$TXT_Y
export GLOSS_PROMPT_PATH_STYLE=$BOLD$TXT_B
export GLOSS_PROMPT_VENV_STYLE=$BOLD$TXT_C
export GLOSS_PROMPT_GIT_STYLE=$BOLD$TXT_M

# Save the starting shell level.
[[ -z ${GLOSS_SHLVL-} ]] && export GLOSS_SHLVL=$SHLVL

# shell level prefix.
export GLOSS_PROMPT_PREFIX_LVL=''
if [[ $SHLVL -gt $GLOSS_SHLVL ]]; then
  export GLOSS_PROMPT_PREFIX_LVL="$(( SHLVL - GLOSS_SHLVL )) "
fi

# Prompt sudo prefix.
export GLOSS_PROMPT_PREFIX_SUDO=''
if [[ -n "${SUDO_USER-}" ]]; then
  export GLOSS_PROMPT_PREFIX_SUDO="$SUDO_USER "
fi

# Prompt user color.
if [[ "${USER-}" == root ]]; then
  export GLOSS_PROMPT_USER_STYLE=$TXT_R
else
  export GLOSS_PROMPT_USER_STYLE=$TXT_G
fi

update_terminal_prompt() {
  local _exit_status=$?

  # Clear custom titles and progress indicators left behind by the previous command.
  printf '\e]1;\a\e]2;\a\e]9;4;0\a'

  # Green prompt if last command exited cleanly (0); otherwise red.
  if [[ $_exit_status -eq 0 ]]; then
    local prompt_symbol_color=$TXT_G
  else
    local prompt_symbol_color=$TXT_R
  fi

  local ssh=''
  if [[ -n "${SSH_TTY-}" ]]; then
    local _ssh_hostname=$(hostname -s)
    local ssh="$GLOSS_PROMPT_SSH_SYMBOL$_ssh_hostname "
  fi

  local venv=''
  [[ -n ${VIRTUAL_ENV-} ]] && local venv="$(basename $(dirname $VIRTUAL_ENV)) "

  local _git=$(git-prompt 2>/dev/null)
  local _git_escaped=${_git//\%/%%} # Double every percent symbol, as that is the escape character for prompt expansion.
  # git-prompt emits a bare fragment; append the separating space only when it is nonempty.
  if [[ -n $_git_escaped ]]; then
    _git_escaped+=' '
  fi

  # For prompt styling, we mostly eschew the ZSH specific escapes in favor of ANSI escape codes.
  # %{ escapes to allow arbitary escape sequences in the prompt; these must not contain visible text that advances the position.
  # This lets us use ANSI color codes rather than the zsh ones.
  # %~ is the current working directory, with $HOME abbreviation.
  # For all ZSH escape codes, see here: http://zsh.sourceforge.net/Doc/Release/Prompt-Expansion.html#Prompt-Expansion.
  PROMPT="\
%{$RST$GLOSS_PROMPT_PREFIX_STYLE%}\
$ssh\
$GLOSS_PROMPT_PREFIX_LVL\
$GLOSS_PROMPT_PREFIX_SUDO\
%{$GLOSS_PROMPT_USER_STYLE%}${USERNAME-} \
%{$GLOSS_PROMPT_PATH_STYLE%}%~ \
%{$GLOSS_PROMPT_VENV_STYLE%}$venv\
%{$GLOSS_PROMPT_GIT_STYLE%}$_git_escaped\
%{$prompt_symbol_color%}$GLOSS_PROMPT_SYMBOL \
%{$RST%}"

  # Continuation prompt.
  PS2="%{$RST$TXT_Y%}%_> %{$RST%}"
}

autoload -Uz add-zsh-hook
add-zsh-hook precmd update_terminal_prompt
