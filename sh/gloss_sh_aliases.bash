# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.


# shell aliases sourced by gloss_env.sh

alias cp='cp -i' # confirm overwrites interactively.
alias mv='mv -i' # confirm overwrites interactively.
alias rm='rm -i' # confirm deletes interactively; encourages use of `del`.

alias venv-create-3.6='python3.6 -m venv ./venv3.6'
alias venv-create-3.7='python3.7 -m venv ./venv3.7'
alias venv-activate-3.6='source ./venv3.6/bin/activate'
alias venv-activate-3.7='source ./venv3.7/bin/activate'


# list all functions defined in this shell environment.
# this must be an alias, rather than a shell script, because declare is a builtin.
# declare -F lists all defined functions with format: declare -f <function-name>.
# cut limits output to just the function name.
alias list_functions='declare -F | cut -d " " -f 3'
