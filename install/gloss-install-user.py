#!/usr/bin/env python3 -B
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# usage: gloss_user_install.py [custom_dst_dir]

# install the user-specific portions (does not require root privileges):
# - bash_profile, bashrc, and bash_setup scripts.

from _gloss_install_common import * # parses arguments, etc.


def append_line_if_missing(path, line):
  assert line.endswith('\n')
  if is_file(path):
    for l in open(path):
      if l == line:
        errSL('skipping:', path)
        return
  errSL('modifying:', path)
  with open(path, 'a') as f:
    writeF(f, '\n# automatically added by gloss-install-user.py\n{}', line)


# make sure that gloss system is installed.
check(
  is_dir(dst_dir),
  'bad gloss dst directory:', dst_dir,
  '\nfirst run gloss-install-sys.py; if using a custom install directory,',
  ' it must be the same for both sys and user installations.'
)

try:
  errL('setting up .bash_setup.bash to use the gloss environment...')

  bash_setup_path =expand_user('~/.bash_setup.bash')  # path to common bash setup file.
  profile_path    =expand_user('~/.bash_profile')   # executed for login shells.
  rc_path         =expand_user('~/.bashrc')         # executed for non-login shells.

  source_env_line   = 'source ' + path_join(dst_dir, 'sh/gloss_env.bash') + '\n' # bash_setup sources gloss_env.
  source_setup_line = 'source ' + bash_setup_path + '\n' # traditional bash files source bash_setup.

  append_line_if_missing(bash_setup_path, source_env_line)

  for p in [profile_path, rc_path]:
    append_line_if_missing(p, source_setup_line)

except OSError as e: # usually permissions.
  errL(e)

