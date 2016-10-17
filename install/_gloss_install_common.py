# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

'common code for the install scripts.'

from os import uname as os_uname
from sys import argv

from pithy.io import check, errSL
from pithy.fs import abs_path, copy_dir_tree, copy_file, is_dir, list_dir, make_dir, make_dirs, path_dir, path_exists, path_join, path_stem, remove_dir_tree


supported_platforms = ['mac']

# gloss uses a single system installation directory for all files, to ease removal and upgrade.
# a custom installation directory can be speficied as an argument to the installation scripts.
# please note that custom directories are not well tested.
install_prefix = '/usr/local'

# parse arguments.
if len(argv) > 2:
  exit('usage: optionally specify a custom installation prefix.')
if len(argv) == 2:
  install_prefix = argv[1]

check(' ' not in install_prefix, "installation prefix contains space.")

# determine the gloss source directory.
src_dir = abs_path(path_join(path_dir(argv[0]), '..'))
check(is_dir(src_dir), 'bad source directory:', src_dir)

dst_dir = path_join(install_prefix, 'gloss')

uname = os_uname()[0].lower()
if uname == 'darwin':
  platform = 'mac'
elif uname == 'linux':
  with open('/etc/issue') as f:
    # get the first word from the issue string (e.g. 'Fedora')
    platform = f.readline().split()[0].lower()
else:
  platform = uname.lower()

errSL('src_dir:', src_dir)
errSL('dst_dir:', dst_dir)
errSL('platform:', platform)

if platform not in supported_platforms:
  errSL('warning: unsupported platform;\n  expected one of', supported_platforms)
