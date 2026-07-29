#!/usr/bin/env bash

set -e

fail() { echo "error: $@" >&2; exit 1; }

dotfiles_dir="dotfiles"

[[ -d "$dotfiles_dir" ]] || fail "gloss dotfiles directory not found: $dotfiles_dir"

# True if the installed file is identical to some committed version of the repo file,
# meaning it was installed by gloss and never customized by the user.
matches_committed_version() {
  local repo_path="$1" installed_path="$2" installed_hash rev
  installed_hash=$(git hash-object "$installed_path" 2>/dev/null) || return 1
  for rev in $(git rev-list HEAD -- "$repo_path" 2>/dev/null); do
    [[ "$(git rev-parse "$rev:$repo_path" 2>/dev/null)" == "$installed_hash" ]] && return 0
  done
  return 1
}

for dir in $(find $dotfiles_dir/* -type d); do
  dot_dir="$HOME/.${dir#$dotfiles_dir/}"
  echo "creating: $dot_dir"
  mkdir -p $dot_dir
done

for path in $(find $dotfiles_dir -type f); do
  dot_path="$HOME/.${path#$dotfiles_dir/}"
  if [[ -L "$dot_path" ]]; then # A legacy symlink installation; -L is true even when the link target is missing, unlike -e.
    if [[ -e "$dot_path" ]] && ! cmp -s "$path" "$dot_path" && ! matches_committed_version "$path" "$dot_path"; then
      echo "customized symlink; skipping: $dot_path"
      continue
    fi
    echo "replacing symlink with copy: $dot_path"
    rm "$dot_path"
    cp "$path" "$dot_path"
  elif [[ -e "$dot_path" ]]; then
    if cmp -s "$path" "$dot_path"; then
      echo "up to date: $dot_path"
    elif matches_committed_version "$path" "$dot_path"; then
      echo "updating: $dot_path"
      cp "$path" "$dot_path"
    else
      echo "customized; skipping: $dot_path"
    fi
  else
    echo "copying: $dot_path"
    cp "$path" "$dot_path"
  fi
done
