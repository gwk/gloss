# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

if [[ -o interactive ]]; then # Guard this to prevent Claude Code from getting tripped up with its weird shell setup.
  alias cp='cp -i' # confirm overwrites interactively.
  alias mv='mv -i' # confirm overwrites interactively.
  alias rm='rm -i' # confirm deletes interactively; encourages use of `del`.
fi

# Aliases for generated bin scripts that are equivalent to simple commands.
[[ -f $GLOSS_DIR/zsh/aliases-generated.zsh ]] && source $GLOSS_DIR/zsh/aliases-generated.zsh
[[ -f $GLOSS_DIR/zsh/aliases-generated-platform.zsh ]] && source $GLOSS_DIR/zsh/aliases-generated-platform.zsh
