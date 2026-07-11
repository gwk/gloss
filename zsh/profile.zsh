# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# .zprofile is sourced for login shells only, after .zshenv and /etc/zprofile.
# Source this file from your .zprofile with the following command:
#   source /opt/gloss/zsh/profile.zsh

# On macOS, /etc/zprofile runs path_helper, which reorders PATH (and MANPATH if set).
# Reestablish the gloss ordering after that; non-login shells source paths.zsh from env.zsh instead.
source ${GLOSS_DIR:-/opt/gloss}/zsh/paths.zsh
