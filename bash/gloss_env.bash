# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# gloss shell environment setup.

# bash environment rules:
#   interactive
#     login: /etc/bash.bashrc, sources .bashrc
#     non-login:/etc/profile, sources first of .bash_profile, .bash_login, .profile
#   non-interactive:
#     $BASH_ENV


prepend_to_search_path() {
  # The first argument is the name of the path variable to prepend to (e.g. PATH or MANPATH).
  # Each subsequent element is a path to prepend.
  # This does not create leading or trailing colons,
  # which would cause '/' to become an implied member of the path.

  # get the path name.
  local _path_name=$1
  shift

  local _path=$($GLOSS_DIR/bin/prepend-to-search-path.py $_path_name $@)

  # NOTE: during shell startup bash will fail to capture the exit code,
  # either due to python not residing in existing PATH or script exit code.
  # Therefore we also check that the output is not empty.
  # Without this check we would inadvertantly set PATH to blank, making the shell less usable.
  if [[ $? != 0 || -z $_path ]]; then
    echo "prepend_to_search_path failed" 1>&2
    return
  fi

  eval export $_path_name="'$_path'"
}


export_if_not_set() {
  local _var_name=$1
  local _new_val=$2

  eval local _existing_val=\$$_var_name

  if [[ -z "$_existing_val" ]]; then
    eval export $_var_name=\"$_new_val\"
  fi
}


# customize shell prompt to show colored string with:
# ssh prefix;
# shell level prefix;
# sudo username;
# username (\u);
# path.

export GLOSS_PS_SYMBOL='$'

gloss_set_prompts() {
  local _exit_status=$?
  GLOSS_PS_PREFIX_STYLE=$TXT_L
  GLOSS_PS_PATH_STYLE=$BOLD$TXT_B
  GLOSS_PS_VENV_STYLE=$BOLD$TXT_C
  GLOSS_PS_GIT_STYLE=$BOLD$TXT_M

  # red prompt if last command was an error, or else green
  if [[ $_exit_status -eq 0 ]]; then
    GLOSS_PS_PROMPT_STYLE=$TXT_G
  else
    GLOSS_PS_PROMPT_STYLE=$TXT_R
  fi
  if [[ -n $VIRTUAL_ENV ]]; then
    GLOSS_PS_PROMPT_VENV=" $(basename $(dirname $VIRTUAL_ENV))"
  else
    GLOSS_PS_PROMPT_VENV=''
  fi

  # bash prompt
  PS1="\[$RST\]\
\[$GLOSS_PS_PREFIX_STYLE\]\
$GLOSS_PS_PREFIX_SSH\
$GLOSS_PS_PREFIX_LVL\
$GLOSS_PS_PREFIX_SUDO\
\[$GLOSS_PS_USER_STYLE\]\u \
\[$GLOSS_PS_PATH_STYLE\]\w\
\[$GLOSS_PS_VENV_STYLE\]$GLOSS_PS_PROMPT_VENV\
\[$GLOSS_PS_GIT_STYLE\]$(git-prompt 2>/dev/null)\
\[$RST\] \
\[$GLOSS_PS_PROMPT_STYLE\]$GLOSS_PS_SYMBOL \
\[$RST\]"

  # bash continuation prompt
  PS2="\[$RST\]\
\[$GLOSS_PS_PROMPT_STYLE\]$GLOSS_PS_SYMBOL \
\[$RST\]"

  # PS3: bash select prompt

  # PS4: bash tracing prompt (set -x)
  #export PS4='+${BASH_SOURCE}:${LINENO}:${FUNCNAME[0]}: '

  $GLOSS_PROMPT_CMDS
}

PROMPT_COMMAND="gloss_set_prompts" # prompt is set dynamically with PROMPT_COMMAND.


# gloss environment not yet set; only set up once.
if [[ -z "$GLOSS_ENV" ]]; then
  export GLOSS_ENV=True

  set -o pipefail
  set -o noclobber

  # default to system-wide installation
  [[ -z "$GLOSS_DIR" ]] && export GLOSS_DIR=/usr/local/gloss

  [[ -d "$GLOSS_DIR" ]] || echo "WARNING: bad GLOSS_DIR definition: $GLOSS_DIR" 1>&2

  # calculate platform string
  GLOSS_PLATFORM=$(uname | tr '[:upper:]' '[:lower:]')
  if [[ "$GLOSS_PLATFORM" == "linux" ]]; then
      issue=$(tr '[:upper:]' '[:lower:]' < /etc/issue) # get the issue, which is 'Fedora etc ...'
      GLOSS_PLATFORM=${issue%% *} # get the first word
  fi
  export GLOSS_PLATFORM

  # save the starting shell level.
  export GLOSS_SHLVL=$SHLVL

  # section symbol string used to denote ssh (note: requires utf-8 support)
  # if this is an ssh session, define the prefix variable to be included in PS1.
  # export this from profile so that it is defined for all subshells.
  if [[ -n "$SSH_TTY" ]]; then
    export GLOSS_PS_PREFIX_SSH='§ '
  else
    export GLOS_PS_PREFIX_SSH=''
  fi

  prepend_to_search_path PATH "$GLOSS_DIR/bin"

  export PAGER=less
  export LESS=FRX
  export CLICOLOR=1 # enable colors in ls.

  export GREP_OPTIONS="--color=auto --binary-files=without-match"
  export GREP_COLOR="4" # underline.
  export HISTIGNORE="&" # colon-separated patterns; & is special case to skip duplicates

  # require many consecutive C-d keypresses to close the shell,
  # so that repeated C-d keypresses intended for readline delete do not accidentally close.
  export IGNOREEOF=32

  export NODE_REPL_MODE="strict"

  # currently unused; would be nice to show only the last n characters of cwd.
  #export GLOSS_PROMPT_DIR_TRIM=32

  # ANSI select graphic rendition (SGR) control sequences.

  export RST='\e[0m' # reset.
  export RST_BOLD='\e[22m'
  export RST_ULINE='\e[24m'
  export RST_BLINK='\e[25m'
  export RST_INVERT='\e[27m'
  export RST_TXT='\e[39m'
  export RST_BG='\e[49m'

  export BOLD='\e[1m'
  export ULINE='\e[4m'
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

  # Utils only need to be sourced once.
  source $GLOSS_DIR/bash/gloss_sh_utils.bash

  # platform specific configuration.
  if [[ "$GLOSS_PLATFORM" == 'darwin' ]]; then
    export EDITOR='code -w "$@"' # use vs code as shell editor.
  fi
fi

# set the following for every shell.

# shell level prefix.
export GLOSS_PS_PREFIX_LVL=''
if [[ $SHLVL -gt $GLOSS_SHLVL ]]; then
  export GLOSS_PS_PREFIX_LVL="$(( SHLVL - GLOSS_SHLVL )) "
fi

# sudo prefix.
export GLOSS_PS_PREFIX_SUDO=''
if [[ -n "$SUDO_USER" ]]; then
  export GLOSS_PS_PREFIX_SUDO="$SUDO_USER "
fi

# prompt user color: red for root, green for normal.
if [[ $(whoami) == root ]]; then
  export GLOSS_PS_USER_STYLE=$TXT_R
else
  export GLOSS_PS_USER_STYLE=$TXT_G
fi

export GLOSS_PROMPT_CMDS=''
if [[ $(type -t update_terminal_cwd) == 'function' ]]; then
  # this is function is defined in mac 10.11 default /etc/bashrc_Apple_Terminal.
  # must be called as a suffix so that gloss-set-prompts sees the value of $? first.
  export GLOSS_PROMPT_CMDS='update_terminal_cwd'
fi

# source alias definitions for every shell instance; apparently aliases cannot be exported.
source $GLOSS_DIR/bash/gloss_sh_aliases.bash

#if [[ $PS1 && -r /usr/local/share/bash-completion/bash_completion ]]; then
  #source /usr/share/bash-completion/bash_completion
  #source $GLOSS_DIR/bash/bash_completion/git-completion.bash
#fi

