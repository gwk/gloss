# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

'common code for the install scripts.'

from os import uname as os_uname
from sys import argv, stderr

from os.path import abspath as abs_path, isdir as is_dir, dirname as path_dir, join as path_join


def errSL(*items): print(*items, file=stderr)


supported_platforms = ['mac', 'linux']

# gloss uses a single system installation directory for all files, to ease removal and upgrade.
# a custom installation directory can be speficied as an argument to the installation scripts.
# please note that custom directories are not well tested.
install_prefix = '/usr/local'

# parse arguments.
if len(argv) > 2:
  exit('usage: optionally specify a custom installation prefix.')
if len(argv) == 2:
  install_prefix = argv[1]

if ' ' in install_prefix: exit("installation prefix contains space.")

# determine the gloss source directory.
src_dir = abs_path(path_join(path_dir(argv[0]), '..'))
if not is_dir(src_dir): exit('bad source directory: ' + src_dir)

dst_dir = path_join(install_prefix, 'gloss')

platform = 'unknown'
distro = ''
uname_info = os_uname()
sysname = uname_info.sysname.lower()
if sysname == 'darwin':
  platform = 'mac'
elif sysname == 'linux':
  platform = 'linux'
  if 'amzn2022' in uname_info.release:
    distro = 'amzn2022'
  else:
    distro = 'unknown'
    errSL('warning: unknown linux distro:', uname_info.release)
else:
  platform = sysname

errSL('src_dir:', src_dir)
errSL('dst_dir:', dst_dir)
errSL('platform:', platform)

if platform not in supported_platforms:
  errSL('warning: unsupported platform;\n  expected one of', supported_platforms)
