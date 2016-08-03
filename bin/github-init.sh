set -e

error() { echo "error:" "$@" 1>&2; exit 1; }

[[ -d .git ]] || git init
if ! git log -1 2> /dev/null; then
  [[ -s .gitignore ]] && exit 'no commits but .gitignore already populated; cannot commit empty .gitignore as first commit.' 
  touch .gitignore
  git add .gitignore
  git commit -m 'initial.'
fi

hub create "$@"
git remote rename origin github
git push -u github master
