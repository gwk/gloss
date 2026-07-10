#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# Usage: gloss_sys_install.py [custom_dst_dir]

from os import (listdir as list_dir, makedirs as make_dirs, mkdir as make_dir, remove as remove_file, replace as replace_file,
  scandir as scan_dir, stat, umask)
from os.path import exists as path_exists, isdir as is_dir, join as path_join, splitext as split_ext
from shutil import copyfile, copytree, rmtree as remove_tree
from stat import S_ISDIR
from subprocess import run

from _gloss_install_common import distro, dst_dir, errSL, platform, src_dir  # Parses arguments, etc.


def main() -> None:
  umask(0o022) # Ensure created files are world-readable and executable.

  try:
    if is_dir(dst_dir):
      errSL('removing old dst_dir contents…')
      for entry in scan_dir(dst_dir):
        path = entry.path
        errSL(' ', path)
        if is_dir(path): remove_tree(path)
        else: remove_file(path)
    else:
      try:
        make_dirs(dst_dir, mode=0o755)
      except OSError as e:
        errSL(f'error: could not make installation directory: {dst_dir}; {e}.')
        errSL(f'Please run `sudo mkdir {dst_dir} and chown as necessary.')
        exit(1)

    platform_txt = f'{platform}\t{distro}'  # Use a tab for default compatibility with `cut`.
    errSL(f'writing platform.txt: {platform_txt}')
    with open(path_join(dst_dir, 'platform.txt'), 'w') as f:
      print(platform_txt, file=f)

    errSL('copying files to dst_dir…')

    # Copy directories.
    sub_dirs = ['zsh']
    for d in sub_dirs:
      src_subdir = path_join(src_dir, d)
      dst_subdir = path_join(dst_dir, d)
      install_tree(src_subdir, dst_subdir)

    # Copy individual files.
    for p in ['pythonstartup.py']:
      src = path_join(src_dir, p)
      dst = path_join(dst_dir, p)
      install_file(src, dst)

    errSL('installing gloss bin...')
    dst_bin_dir = path_join(dst_dir, 'bin')
    make_dir(dst_bin_dir, mode=0o755)


    def install_bin_dir(bin_dir:str) -> None:
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
          errSL('notice:', name, 'already installed at:', res.stdout.decode(), '\n  shadowed by:', dst_path)
        install_file(src_path, dst_path)


    # Install cross-platform bin dir.
    cross_bin_dir = path_join(src_dir, 'bin')
    install_bin_dir(cross_bin_dir)

    # Install platform-specific bin dir.
    os_bin_dir = path_join(src_dir, 'os', platform, 'bin')
    if is_dir(os_bin_dir):
      install_bin_dir(os_bin_dir)

    errSL('generating additional scripts…')

    gen_dir = path_join(src_dir, 'gen')
    gen_cmd = path_join(gen_dir, 'gen-bins.py')
    bins_path = path_join(gen_dir, 'bins.txt')
    bins_platform_path = path_join(gen_dir, f'bins-{platform}.txt')

    run([gen_cmd, bins_path, dst_bin_dir], check=True)

    if path_exists(bins_platform_path):
      run([gen_cmd, bins_platform_path, dst_bin_dir], check=True)
    else:
      errSL('no platform specifics to generate found at:', bins_platform_path)

    run(['chmod', '-R', '+rx', dst_bin_dir])

    install_sudoers_secure_path(dst_bin_dir)

  except OSError as e: # Usually a permissions problem.
    errSL(e)
    exit(1)


def install_sudoers_secure_path(dst_bin_dir:str) -> None:
  '''
  Configure the sudoers `secure_path` to contain only root-owned directories that are not group/other-writable.
  This excludes user-owned locations (e.g. /opt/homebrew, /opt/py, /opt/rust)
  so that sudo never resolves commands from user-writable directories.
  The candidate ordering mirrors the PATH ordering established by zsh/paths.zsh.
  '''
  sudoers_dir = '/etc/sudoers.d'
  if not is_dir(sudoers_dir):
    errSL('warning: no sudoers.d directory; skipping secure_path configuration:', sudoers_dir)
    return
  candidates = [
    '/usr/local/bin',
    '/usr/bin',
    '/bin',
    '/usr/sbin',
    '/sbin',
    dst_bin_dir,
  ]
  secure_dirs = [p for p in candidates if is_root_secure_dir(p)]
  errSL('sudoers secure_path:', *secure_dirs)
  content = 'Defaults secure_path="{}"\n'.format(':'.join(secure_dirs))
  dst_path = path_join(sudoers_dir, 'gloss-secure-path')
  tmp_path = dst_path + '.tmp' # sudo ignores file names containing a dot, so a partial or invalid write is never active.
  with open(tmp_path, 'w') as f:
    f.write(content)
  run(['chmod', '0440', tmp_path], check=True)
  res = run(['visudo', '-cf', tmp_path])
  if res.returncode != 0:
    remove_file(tmp_path)
    errSL('error: generated secure_path sudoers file failed visudo check; not installed.')
    exit(1)
  replace_file(tmp_path, dst_path)


def is_root_secure_dir(path:str) -> bool:
  'Return True if `path` is a directory owned by root and not writable by group or other.'
  try: st = stat(path) # Follows symlinks.
  except OSError: return False
  return S_ISDIR(st.st_mode) and st.st_uid == 0 and not (st.st_mode & 0o022)


def install_file(src:str, dst:str) -> None:
  '''
  Copy a file and then set a+rX permissions on the copied file.
  '''
  errSL(src, '=>', dst)
  copyfile(src, dst)
  run(['chmod', 'a+rX', dst], check=True)


def install_tree(src:str, dst:str) -> None:
  '''
  Copy a directory tree and then set a+rX permissions on eveyrthing in the copied tree.
  '''
  errSL(src, '=>', dst)
  copytree(src, dst, dirs_exist_ok=True)
  run(['chmod', '-R', 'a+rX', dst], check=True)


def path_stem(path:str) -> str: return split_ext(path)[0]


if __name__ == '__main__': main()
