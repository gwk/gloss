#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# Install all files from dotfiles/ as copies under $HOME, prefixing each top-level name with a dot.
# Run from the repository root via the justfile.

set -e

export BOLD=$'\e[1m'
export RST_BOLD=$'\e[22m'

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

# Make directories.
for dir in $(find $dotfiles_dir/* -type d); do
  dot_dir="$HOME/.${dir#$dotfiles_dir/}"
  echo "creating: $dot_dir"
  mkdir -p $dot_dir
done

# Check and copy files.
for path in $(find $dotfiles_dir -type f); do
  dot_path="$HOME/.${path#$dotfiles_dir/}"
  if [[ -L "$dot_path" ]]; then # A legacy symlink installation; -L is true even when the link target is missing, unlike -e.
    if [[ -e "$dot_path" ]] && ! cmp -s "$path" "$dot_path" && ! matches_committed_version "$path" "$dot_path"; then
      printf '%scustomized symlink; skipping: %s%s\n' "$BOLD" "$dot_path" "$RST_BOLD"
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
      printf '%scustomized; skipping: %s%s\n' "$BOLD" "$dot_path" "$RST_BOLD"
    fi
  else
    echo "copying: $dot_path"
    cp "$path" "$dot_path"
  fi
done
