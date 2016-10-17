# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# gloss shell environment setup.

# bash environment rules:
#   interactive
#     login: /etc/bash.bashrc, sources .bashrc
#     non-login:/etc/profile, sources first of .bash_profile, .bash_login, .profile
#   non-interactive:
#     $BASH_ENV


prepend_to_search_paths() {
  # The first argument is the name of the path variable to prepend to (e.g. PATH or MANPATH).
  # Each subsequent element is a path to prepend.
  # This does not create leading or trailing colons,
  # which would cause '/' to become an implied member of the path.

  # get the path name.
  local _path_name=$1
  shift

  local _path=$($GLOSS_DIR/sh/prepend-to-search-path.py $_path_name $@)

  # NOTE: during shell startup bash will fail to capture the exit code,
  # either due to python3 not residing in existing PATH or script exit code.
  # Therefore we also check that the output is not empty.
  # Without this check we would inadvertantly set PATH to blank, making the shell less usable.
  if [[ $? != 0 || -z $_path ]]; then
    echo "prepend_to_search_paths failed" 1>&2
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

export GLOSS_PROMPT_CMDS='' # can be modified in subshells.

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


# gloss environment not yet set; only set up once.
if [[ -z "$GLOSS_ENV" ]]; then

  set -o pipefail
  # TODO: set -u ? currently requires fixing usage VIRTUAL_ENV at least.
  # set -C: prevents output redirection from overwriting.

  export GLOSS_ENV=True

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
  fi

  # prompt is set dynamically with PROMPT_COMMAND.
  export PROMPT_COMMAND="gloss_set_prompts"

  prepend_to_search_paths PATH \
  "$GLOSS_DIR/bin" \
  /usr/local/{cmake,git,graphviz,heroku,nasm,py,ruby,rust,xctool}/bin \
  /usr/local/llvm/3.8.0/bin \
  /opt/libjpeg-turbo/bin \
  /usr/local/bin \
  /Library/Frameworks/Python.framework/Versions/3.5/bin \
  /Library/Frameworks/Python.framework/Versions/2.7/bin \
  /Developer/NVIDIA/CUDA-7.5/bin

  prepend_to_search_paths MANPATH \
  /usr/local/{cmake,git,graphviz,heroku,nasm,py,ruby,rust,xctool}/share/man \
  /usr/local/llvm/3.8.0/share/man \
  /opt/libjpeg-turbo/share/man \
  /usr/local/share/man \
  /usr/share/man \
  /Library/Frameworks/Python.framework/Versions/2.7/share/man \
  /Library/Frameworks/Python.framework/Versions/3.5/share/man \
  /Applications/Xcode-beta.app/Contents/Developer/usr/share/man \
  /Applications/Xcode-beta.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/share/man \
  /Applications/Xcode.app/Contents/Developer/usr/share/man \
  /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/share/man \

  # append paths not owned by root to the back of the paths for safety.
  if [[ -n "$GLOSS_OCAML" ]]; then
    export PATH=$PATH:~/.opam/$GLOSS_OCAML/bin
    export MANPATH=$MANPATH:~/.opam/$GLOSS_OCAML/man
    export CAML_LD_LIBRARY_PATH=~/.opam/$GLOSS_OCAML/lib/stublibs
    export PERL5LIB=~/.opam/$GLOSS_OCAML/lib/perl5
    export OCAML_TOPLEVEL_PATH=~/.opam/$GLOSS_OCAML/lib/toplevel
    export OPAMUTF8MSGS=1
  fi

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
  export NLTK_DATA=~/external/nltk_data

  # currently unused; would be nice to show only the last n characters of cwd.
  #export GLOSS_PROMPT_DIR_TRIM=32

  # exports only need to be sourced once.
  source $GLOSS_DIR/sh/gloss_sh_exports.bash

  # platform specific configuration.
  if [[ "$GLOSS_PLATFORM" == 'darwin' ]]; then
    export EDITOR='code -w "$@"' # use vs code as shell editor.
  fi
fi

# set the following for every shell.

# shell level prefix.
if [[ $SHLVL -gt $GLOSS_SHLVL ]]; then
  export GLOSS_PS_PREFIX_LVL="$(( SHLVL - GLOSS_SHLVL )) "
else
  export GLOSS_PS_PREFIX_LVL=""
fi

# sudo prefix.
if [[ -n "$SUDO_USER" ]]; then
  export GLOSS_PS_PREFIX_SUDO="$SUDO_USER "
fi

# prompt user color: red for root, green for normal.
if [[ $(whoami) == root ]]; then
  export GLOSS_PS_USER_STYLE=$TXT_R
else
  export GLOSS_PS_USER_STYLE=$TXT_G
fi

if [[ $(type -t update_terminal_cwd) == 'function' ]]; then
  # this is function is defined in mac 10.11 default /etc/bashrc_Apple_Terminal.
  # must be called as a suffix so that gloss-set-prompts sees the value of $? first.
  GLOSS_PROMPT_CMDS='update_terminal_cwd'
fi

# source alias definitions for every shell instance; apparently aliases cannot be exported.
source $GLOSS_DIR/sh/gloss_sh_aliases.bash

#if [[ $PS1 && -r /usr/local/share/bash-completion/bash_completion ]]; then
  #source /usr/share/bash-completion/bash_completion
  #source $GLOSS_DIR/sh/bash_completion/git-completion.bash
#fi

