# Copyright 2010 George King. Permission to use this file is granted in license-gloss.txt.


# shell aliases sourced by gloss_env.sh

alias mv='mv -i' # confirm overwrites interactively.
alias cp='cp -i' # confirm overwrites interactively.
alias venv-activate='source venv/bin/activate' # venv activate.


# list all functions defined in this shell environment.
# this must be an alias, rather than a shell script, because declare is a builtin.
# declare -F lists all defined functions with format: declare -f <function-name>.
# cut limits output to just the function name.
alias list_functions='declare -F | cut -d " " -f 3'
