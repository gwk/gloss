set -e

fail() { echo "error: $@" >&2; exit 1; }

dotfiles_dir="dotfiles"

[[ -d "$dotfiles_dir" ]] || fail "gloss dotfiles directory not found: $dotfiles_dir"

for dir in $(find $dotfiles_dir/* -type d); do
  dot_dir="$HOME/.${dir#$dotfiles_dir/}"
  echo "creating: $dot_dir"
  mkdir -p $dot_dir
done

for path in $(find $dotfiles_dir -type f); do
  abs_path="$PWD/$path"
  dot_path="$HOME/.${path#$dotfiles_dir/}"
  if [[ -e "$dot_path" ]]; then
    echo "already exists: $dot_path"
    continue
  fi
  echo "linking: $dot_path -> $abs_path"
  ln -s "$abs_path" "$dot_path"
done
