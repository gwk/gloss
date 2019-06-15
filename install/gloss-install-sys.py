#!/usr/bin/env python3 -B
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# usage: gloss_sys_install.py [custom_dst_dir]

from _gloss_install_common import * # parses arguments, etc.
from pithy.task import * # TODO: remove pithy dependency.
from os import symlink
from os.path import exists as path_exists


def main():
  try:
    if is_dir(dst_dir):
      errSL('removing old dst_dir...')
      remove_dir_contents(dst_dir)
    make_dirs(dst_dir)

    errSL('copying files to dst_dir...')

    # Copy directories.
    sub_dirs = ['sh']
    for d in sub_dirs:
      src_subdir = path_join(src_dir, d)
      dst_subdir = path_join(dst_dir, d)
      errSL(src_subdir, '=>', dst_subdir)
      copy_dir_tree(src_subdir, dst_subdir)

    errSL('installing gloss bin...')
    dst_bin_dir = path_join(dst_dir, 'bin')
    make_dir(dst_bin_dir)


    def install_bin_dir(bin_dir):
      errSL('install_bin_dir:', bin_dir)

      for src in list_dir(bin_dir):
        name = path_stem(src)
        if not name or name.startswith('.'):
          errSL('skipping', name)
          continue
        src_path = path_join(bin_dir, src)
        dst_path = path_join(dst_bin_dir, name)
        status, existing = runCO(['which', name])
        if status == 0:
          errSL('notice:', name, 'already installed at:', existing, '\n  shadowed by:', dst_path)

        copy_file(src_path, dst_path)


    # install cross-platform bin dir.
    install_bin_dir(path_join(src_dir, 'bin'))

    # install platform-specific bin dir.
    os_bin_dir = path_join(src_dir, 'os', platform, 'bin')
    if is_dir(os_bin_dir):
      install_bin_dir(os_bin_dir)

    errSL('generating additional scripts...')

    gen_dir       = path_join(src_dir, 'gen')
    gen_cmd       = path_join(gen_dir, 'gen-bins.py')
    bins_path     = path_join(gen_dir, 'bins.txt')
    bins_os_path  = path_join(gen_dir, 'bins-{}.txt'.format(platform))

    run([gen_cmd, bins_path, dst_bin_dir])

    if path_exists(bins_os_path):
      run([gen_cmd, bins_os_path, dst_bin_dir])
    else:
      errSL('no platform specifics to gen found at:', bins_os_path)

    # On mac, create a symlink for python3 that points to the MacOS/Python execuctable,
    # which is appears not to perform the extra exec that python3 does, and is thus more amenable to debugging under lldb.
    python_exe = '/Library/Frameworks/Python.framework/Versions/3.7/Resources/Python.app/Contents/MacOS/Python'
    if platform == 'mac' and path_exists(python_exe):
      python3 = path_join(dst_dir, 'bin', 'python3')
      errSL(f'adding python3 symlink: {python3} -> {python_exe}')
      symlink(python_exe, python3)


  except OSError as e: # usually a permissions problem.
    errSL(e)
    exit(1)


if __name__ == '__main__': main()
