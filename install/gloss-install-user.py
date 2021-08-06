#!/usr/bin/env python3 -B
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# Usage: gloss_user_install.py [custom_dst_dir]

# Install the user-specific portions (does not require root privileges).

from os import makedirs
from os.path import expanduser as expand_user, isfile as is_file, isdir as is_dir, join as path_join
from shutil import copy2 as copy_file
from _gloss_install_common import errSL, dst_dir, src_dir # parses arguments, etc.
import site


def main():
  # make sure that gloss system is installed.
  if not is_dir(dst_dir):
    errSL('bad gloss directory:', dst_dir,
      '\nfirst run gloss-install-sys.py; if using a custom install directory,'
      ' it must be the same for both sys and user installations.')
    exit(1)

  try:
    errSL('setting up bash to use the gloss environment...')
    source_env_line   = 'source ' + path_join(dst_dir, 'bash/gloss_env.bash') + '\n'
    for p in ['~/.bash_profile', '~/.bashrc']: # Login and (interactive, nonlogin) respectively.
      append_line_if_missing(expand_user(p), source_env_line)

    # TODO: automatically set up zsh as well.

    install_usercustomize()

  except OSError as e: # usually permissions.
    exit(e)


def install_usercustomize():
  site_packages_dir = site.getusersitepackages()
  name = 'usercustomize.py'
  src = path_join(src_dir, name)
  dst = path_join(site_packages_dir, name)
  errSL('installing:', src, '->', dst)
  makedirs(site_packages_dir, exist_ok=True)
  copy_file(src, dst)



def append_line_if_missing(path, line):
  assert line.endswith('\n')
  if is_file(path):
    for l in open(path):
      if l == line:
        errSL('already set up:', path)
        return
  errSL('modifying:', path)
  with open(path, 'a') as f:
    f.write('\n# Automatically added by gloss-install-user.py.\n')
    f.write(line)


if __name__ == '__main__': main()
