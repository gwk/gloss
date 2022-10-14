set -e

fail() { echo "error: $@" >&2; exit 1; }

dotfiles_dir="$PWD/dotfiles"

[[ -d "$dotfiles_dir" ]] || fail "gloss dotfiles directory not found: $dotfiles_dir"

dotfiles=$(ls -A "$dotfiles_dir")

cd "$HOME"

for name in $dotfiles; do
  dot_path="$HOME/.$name"
  if [[ -e "$dot_path" ]]; then
    echo "skipping: $dot_path; already exists."
    continue
  fi
  echo "linking: $dot_path -> $dotfiles_dir/$name"
  ln -s "$dotfiles_dir/$name" "$dot_path"
done
