set -e

if [[ -z "$1" ]]; then
  echo 'Please specify a Python version.'
  exit 1
else
  python$1 -m venv ./venv
fi
