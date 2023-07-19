#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# Usage: gloss_sys_install.py [custom_dst_dir]

from os import listdir as list_dir, makedirs as make_dirs, mkdir as make_dir, remove as remove_file, scandir as scan_dir
from os.path import exists as path_exists, isdir as is_dir, join as path_join, splitext as split_ext
from shutil import copy2 as copy_file, copytree, rmtree as remove_tree
from subprocess import run

from _gloss_install_common import distro, dst_dir, errSL, platform, src_dir  # Parses arguments, etc.


def main():
  try:
    if is_dir(dst_dir):
      errSL('removing old dst_dir contents...')
      for entry in scan_dir(dst_dir):
        path = entry.path
        errSL(path)
        if is_dir(path): remove_tree(path)
        else: remove_file(path)
    else:
      try: make_dirs(dst_dir) # Note: may fail if /usr/local is owned by root (i.e. has not been tampered with by homebrew).
      except OSError as e:
        errSL(f'error: could not make installation directory: {dst_dir}; {e}.')
        errSL(f'Please run `sudo mkdir {dst_dir} && sudo chown [username] {dst_dir}')
        exit(1)

    platform_txt = f'{platform}\t{distro}'  # Use a tab for default compatibility with `cut`.
    errSL(f'writing platform.txt: {platform_txt}')
    with open(path_join(dst_dir, 'platform.txt'), 'w') as f:
      print(platform_txt, file=f)

    errSL('copying files to dst_dir...')

    # Copy directories.
    sub_dirs = ['bash', 'zsh']
    for d in sub_dirs:
      src_subdir = path_join(src_dir, d)
      dst_subdir = path_join(dst_dir, d)
      errSL(src_subdir, '=>', dst_subdir)
      copytree(src_subdir, dst_subdir)

    for p in ['pythonstartup.py']:
      src = path_join(src_dir, p)
      dst = path_join(dst_dir, p)
      errSL(src, '=>', dst)
      copy_file(src, dst)

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
        res = run(['which', name], capture_output=True)
        if res.returncode == 0:
          errSL('notice:', name, 'already installed at:', res.stdout, '\n  shadowed by:', dst_path)

        copy_file(src_path, dst_path)


    # Install cross-platform bin dir.
    install_bin_dir(path_join(src_dir, 'bin'))

    # Install platform-specific bin dir.
    os_bin_dir = path_join(src_dir, 'os', platform, 'bin')
    if is_dir(os_bin_dir):
      install_bin_dir(os_bin_dir)

    errSL('generating additional scripts...')

    gen_dir       = path_join(src_dir, 'gen')
    gen_cmd       = path_join(gen_dir, 'gen-bins.py')
    bins_path     = path_join(gen_dir, 'bins.txt')
    bins_os_path  = path_join(gen_dir, 'bins-{}.txt'.format(platform))

    run([gen_cmd, bins_path, dst_bin_dir]).check_returncode()

    if path_exists(bins_os_path):
      run([gen_cmd, bins_os_path, dst_bin_dir]).check_returncode()
    else:
      errSL('no platform specifics to gen found at:', bins_os_path)

  except OSError as e: # Usually a permissions problem.
    errSL(e)
    exit(1)


def path_stem(path:str) -> str: return split_ext(path)[0]


if __name__ == '__main__': main()
