# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# Locate package data through Python's import machinery, including editable installs.
# Override GLOSS_PITHY_PYTHON to select a specific environment. Do not use uv run here:
# shell startup should neither depend on the current project nor sync an environment.
() {
  local pithy_dir
  pithy_dir=$("${GLOSS_PITHY_PYTHON:-python3}" -P -c '
from importlib.util import find_spec
spec = find_spec("pithy")
if spec is not None and spec.origin:
  print(spec.origin.rpartition("/")[0])
' 2>/dev/null) || return 0
  [[ -n $pithy_dir && -r $pithy_dir/zsh/pithy-cmdparse-completion.zsh &&
    -r $pithy_dir/zsh/pithy-cmdparse-module-completion.zsh ]] || return 0
  source "$pithy_dir/zsh/pithy-cmdparse-completion.zsh"
  source "$pithy_dir/zsh/pithy-cmdparse-module-completion.zsh"
}
