
alias pym='python -m' # run python module.

alias sqlite='sqlite3'


if [[ -o interactive ]]; then # Guard this to prevent Claude Code from getting tripped up with its weird shell setup.
  alias cp='cp -i' # confirm overwrites interactively.
  alias mv='mv -i' # confirm overwrites interactively.
  alias rm='rm -i' # confirm deletes interactively; encourages use of `del`.
fi
