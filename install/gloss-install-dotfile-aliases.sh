set -e

fail() { echo "error: $@" >&2; exit 1; }

dotfiles_dir="$PWD/dotfiles"

[[ -d "$dotfiles_dir" ]] || fail "gloss dotfiles directory not found: $dotfiles_dir"

dotfiles=$(ls -A "$dotfiles_dir")

cd "$HOME"

for name in $dotfiles; do
  dotname=".$name"
  if [[ -e $dotname ]]; then
    echo "skipping: $dotname; already exists."
    continue
  fi
  echo "linking: $dotname -> $dotfiles_dir/$name"
  ln -s "$dotfiles_dir/$name" "$dotname"
done
