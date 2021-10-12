#!/usr/bin/env python3

from argparse import ArgumentParser
from os import getcwd
from os.path import exists as path_exists, expanduser as expand_user, isabs as is_abs, isdir as is_dir
from subprocess import run
from sys import stderr
from typing import Any


def main() -> None:
  parser = ArgumentParser(description='Sync one or more directories to or from a remote, assuming the same directory structure relative to user HOME.')
  parser.add_argument('-src', help='Name of remote to sync files to.')
  parser.add_argument('-dst', help='Name of remote to sync files from.')
  parser.add_argument('paths', nargs='+')
  args = parser.parse_args()

  src = args.src
  dst = args.dst
  home_dir_slash = expand_user('~/')
  curr_dir = getcwd()

  print(src or '<local>', '->', dst or '<local>')
  for path in args.paths:
    path = expand_user(path)
    if path_exists(path) and not is_dir(path):
      errSL('error: local path is not a directory:', path)
      continue
    if not path.endswith('/'):
      path += '/'

    if not is_abs(path):
      path = f'{curr_dir}/{path}'

    remote_path = path
    if remote_path.startswith(home_dir_slash):
      remote_path = '~/' + remote_path.removeprefix(home_dir_slash)

    src_str = f'{src}:{remote_path}' if src else path
    dst_str = f'{dst}:{remote_path}' if dst else path
    cmd = ['rsync',  '-a', '-v', src_str, dst_str]
    print(*cmd)
    run(cmd)


def errSL(*args:Any) -> None: print(*args, file=stderr)


if __name__ == '__main__': main()
