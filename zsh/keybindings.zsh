# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

bindkey '^[[Z' reverse-menu-complete # Bind shift-tab to reverse-step through completion options.

bindkey -r '^J' # Unbind Ctrl-J, which defaults to redundant accept-line (same as Ctrl-M, which is also the Enter key).

# Browse the path at the cursor with fzf, listing one directory level at a time.
fzf-path-completion() {
  setopt localoptions no_aliases
  local directory='' entry selected response key completion='' query=${(Q)PREFIX}
  local picker_status
  local -a entries
  if [[ $PREFIX == */* ]]; then
    directory=${(Q)PREFIX}
    directory=${directory%/*}/
    directory=${directory/#\~\//$HOME/}
    compset -P '*/'
    query=${(Q)PREFIX}
  fi
  while true; do
    entries=()
    for entry in "$directory"*(ND); do
      if [[ -d $entry ]]; then
        entries+=("${entry:t}/")
      else
        entries+=("${entry:t}")
      fi
    done
    entries+=('./' '../')
    picker_status=0
    response=$(printf '%s\0' "${entries[@]}" |
      fzf --read0 --print0 --no-multi --no-print-query --no-expect --expect=tab,esc \
        --height=40% --reverse --scheme=path --query="$query" --prompt="${directory:-./}> " \
        --header='Enter: finish. Tab: complete component. Esc: keep completed path. Ctrl-C: cancel.') || picker_status=$?
    key=${response%%$'\0'*}
    if [[ $key == esc ]]; then
      [[ -n $completion ]] || return 0
      break
    fi
    (( picker_status == 0 )) || return $picker_status
    selected=${response#*$'\0'}
    selected=${selected%$'\0'}
    [[ -n $selected ]] || return
    if [[ $key != tab ]]; then
      completion+=$selected
      break
    fi
    if [[ $selected == */ ]]; then
      completion+=$selected
      directory+=$selected
      query=''
    else
      query=$selected
    fi
  done
  if [[ $completion == */ ]]; then
    compadd -U -i "$IPREFIX" -I "$ISUFFIX" -S '' -- "$completion"
  else
    compadd -U -i "$IPREFIX" -I "$ISUFFIX" -- "$completion"
  fi
}


# Enable fzf integration, keeping Ctrl-T for transposition and using Ctrl-S for path completion.
if (( $+commands[fzf] )); then
  source <(fzf --zsh)
  bindkey '^T' transpose-chars
  zle -C fzf-path-completion complete-word fzf-path-completion
  bindkey '^S' fzf-path-completion
fi

stty discard undef # Disable tty output discard; Ctrl-O.
stty dsusp undef # Disable delayed suspend; Ctrl-Y.
stty kill undef # Disable tty kill-line; Ctrl-U.
stty lnext undef # Disable tty literal-next character; Ctrl-V.
stty quit undef # Disable SIGQUIT character; Ctrl-\.
stty reprint undef # Disable tty line reprint; Ctrl-R.
stty werase undef # Disable tty erase-word; Ctrl-W.

unsetopt FLOW_CONTROL # Disable software flow control (stop/XOFF, start/XON): frees Ctrl-S, Ctrl-Q.
