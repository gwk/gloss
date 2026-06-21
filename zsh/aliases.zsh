# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

alias sqlite='sqlite3'


if [[ -o interactive ]]; then # Guard this to prevent Claude Code from getting tripped up with its weird shell setup.
  alias cp='cp -i' # confirm overwrites interactively.
  alias mv='mv -i' # confirm overwrites interactively.
  alias rm='rm -i' # confirm deletes interactively; encourages use of `del`.
fi

# clang.

alias clang-parse='clang -fsyntax-only -Weverything'
alias clang-pp='clang -o - -E'
alias clang-as='clang -o - -S'
alias clang-ir='clang -o - -S -emit-llvm'
alias clang-ast-dump='clang -cc1 -ast-dump'


# git.

alias ga='git add'

alias gd='git diff'
alias gds='git diff --staged'

# git log format notes
# C: color function
# h: abbreviated commit hash
# cd: committer date
# d: ref names
# s: subject

alias gl='git log --format="%C(cyan)%ad %C(blue)%cd %C(yellow)%h %C(cyan)%an %C(auto)%d %s" --date=iso'
alias gl1='git log --format="%C(cyan)%ad %C(blue)%cd %C(yellow)%h %C(cyan)%an %C(auto)%d %s" --date=iso -1'

alias glm='git log'
alias glm1='git log -1'

# Note: -m flag "makes the merge commits show the full diff like regular commits"; documented in git-log "Diff Formatting".
alias glv='git log --name-status --format=fuller -m'
alias glv1='git log --name-status --format=fuller -m -1'

alias gls='git ls-files'

alias gm='git merge'
alias gms='git merge --squash'
alias gmffo='git merge --ff-only'

alias gpull='git pull'
alias gpush='git push'
alias gpu='git push -u'

alias gr='git rebase'
alias gra='git rebase --abort'
alias grc='git rebase --continue'
alias gri='git rebase --interactive'
alias grscp='git rebase --show-current-patch'
alias grm='git rebase main'

alias gsc='git switch --create'

alias gsh='git show'
alias gshw='git show --color-words'
alias gst='git status --short --branch'

alias gtags='git tag -l'

# python.
alias pym='python -m' # run python module.
alias py='PYTHONSTARTUP=$GLOSS_DIR/pythonstartup.py python3 -q'
alias pdb='python3 -m pdb' # run a python file using pdb.

# file hashes.
alias sha1='openssl dgst -sha1'
alias sha224='openssl dgst -sha224'
alias sha256='openssl dgst -sha256'
alias sha384='openssl dgst -sha384'
alias sha512='openssl dgst -sha512'
