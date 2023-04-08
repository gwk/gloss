if [[ "$1" == '-y' ]]; then
  shift;
  for path in "$@"; do truncate -s 0 "$path"; done
else
  for path in "$@"; do
    confirm "empty '$path'" && truncate -s 0 "$path";
  done
fi
