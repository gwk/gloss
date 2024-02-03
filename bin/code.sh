# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.


# Workaround https://github.com/microsoft/vscode/issues/204005.
# Unset NODE_* env vars that cause warnings.
# https://github.com/electron/electron/blob/2ebaebb603620f18ba231bda684f9af392c76923/shell/app/node_main.cc#L144
for node_env_var in $(env | grep -E '^NODE_\w+' --only-matching); do
  unset $node_env_var
done

Contents='/Applications/Visual Studio Code.app/Contents'
ELECTRON_RUN_AS_NODE=1 exec "$Contents/MacOS/Electron" "$Contents/Resources/app/out/cli.js" "$@"
