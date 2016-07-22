#!/usr/bin/env python3 -B
# Copyright 2010 George King. Permission to use this file is granted in license-gloss.txt.

# usage: gloss_sys_install.py [custom_dst_dir]

from _gloss_install_common import * # parses arguments, etc.
from pithy.task import *

try:
  if is_dir(dst_dir):
    errSL('removing old dst_dir...')
    remove_dir_tree(dst_dir)
  make_dirs(dst_dir)

  errSL('copying files to dst_dir...')

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
    contents = list_dir(bin_dir)

    for src in contents:
      src_path = path_join(bin_dir, src)
      name = path_stem(src)
      
      if not name or name.startswith('.'):
        errSL('skipping', name)
        continue
      
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
    install_bin_dir(os_bin_dir) # platform-specific bin dir
  
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

except OSError as e: # usually a permissions problem.
  errSL(e)
  exit(1)
