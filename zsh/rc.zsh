# zshrc is sourced for interactive shells.


setopt interactive_comments # Allows typing or pasting a comment into the interactive shell.
setopt noclobber
setopt pipefail

zmodload zsh/nearcolor # Approximate 24 bit color as necessary.


export LESS=FRX
export CLICOLOR=1 # Enable colors in ls.

export GREP_OPTIONS="--color=auto --binary-files=without-match"
export GREP_COLOR="4" # Grep highlights matches with underline.

export NODE_REPL_MODE=strict


# Command prompt customization.

# The user can override these at any time.
export GLOSS_PROMPT_SYMBOL='$'
export GLOSS_PROMPT_SSH_SYMBOL='§'
export GLOSS_PROMPT_PREFIX_STYLE=$TXT_Y
export GLOSS_PROMPT_PATH_STYLE=$BOLD$TXT_B
export GLOSS_PROMPT_VENV_STYLE=$BOLD$TXT_C
export GLOSS_PROMPT_GIT_STYLE=$BOLD$TXT_M

# Save the starting shell level.
[[ -z $GLOSS_SHLVL ]] && export GLOSS_SHLVL=$SHLVL

# shell level prefix.
export GLOSS_PROMPT_PREFIX_LVL=''
if [[ $SHLVL -gt $GLOSS_SHLVL ]]; then
  export GLOSS_PROMPT_PREFIX_LVL="$(( SHLVL - GLOSS_SHLVL )) "
fi

# Prompt sudo prefix.
export GLOSS_PROMPT_PREFIX_SUDO=''
if [[ -n "$SUDO_USER" ]]; then
  export GLOSS_PROMPT_PREFIX_SUDO="$SUDO_USER "
fi

# Prompt user color.
if [[ $(whoami) == root ]]; then
  export GLOSS_PROMPT_USER_STYLE=$TXT_R
else
  export GLOSS_PROMPT_USER_STYLE=$TXT_G
fi

update_terminal_prompt() {
  local exit_status=$?

  # Green prompt if last command exited cleanly (0); otherwise red.
  if [[ $_exit_status -eq 0 ]]; then
    local prompt_symbol_color=$TXT_G
  else
    local prompt_symbol_color=$TXT_R
  fi

  local ssh=''
  [[ -n "$SSH_TTY" ]] && local ssh="$GLOSS_PROMPT_SSH_SYMBOL "

  local venv=''
  [[ -n $VIRTUAL_ENV ]] && local venv="$(basename $(dirname $VIRTUAL_ENV)) "

  local _git=$(git-prompt 2>/dev/null)
  local _git_escaped=${_git/\%/%%} # Double any percent symbols, as that is the escape character for prompt expansion.

  # %{ escapes to allow arbitary escape sequences in the prompt; these must not contain visible text that advances the position.
  # This lets us use ANSI color codes rather than the zsh ones.
  # %(<N>L..) is the ternary test against the current SHLVL.
  # %(!..) is the ternary test for escalated privileges.
  # %(?..) is the ternary test for last exit code.
  # %n is $USERNAME.
  # %~ is the current working directory, with $HOME abbreviation.
  PROMPT="\
%{$RST$GLOSS_PROMPT_PREFIX_STYLE%}\
$ssh\
$GLOSS_PROMPT_PREFIX_LVL\
$GLOSS_PROMPT_PREFIX_SUDO\
%{$GLOSS_PROMPT_USER_STYLE%}$USERNAME \
%{$GLOSS_PROMPT_PATH_STYLE%}%~ \
%{$GLOSS_PROMPT_VENV_STYLE%}$venv\
%{$GLOSS_PROMPT_GIT_STYLE%}$_git_escaped\
%{$prompt_symbol_color%}$GLOSS_PROMPT_SYMBOL \
%{$RST%}"

  # Continuation prompt.
  #PS2="%{$RST$TXT_Y$GLOSS_PROMPT_SYMBOL$RST%}"
}

precmd_functions=(
  update_terminal_prompt
  update_terminal_cwd
)
# update_terminal_cwd is provided by macOS. # TODO: conditionally add for mac, or define it for others?


# Disable paste highlighting.
export zle_highlight=(region:standout special:standout suffix:bold isearch:underline paste:none)


# List all aliases/functions defined in this shell environment.
# These are stored in associative arrays; -k gives us keys only; -o sorts.
list-aliases() { print -c ${(ko)aliases} }
list-functions() { print -c ${(ko)functions} }
