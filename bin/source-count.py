#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# gather statistics about source files in a directory tree.

import os
import re

from argparse import ArgumentParser
from collections import Counter
from os.path import splitext as split_ext, basename as path_name, join as path_join
from sys import stderr


ignored_dirs = {'_build', 'build', '.git', '.hg', '.svn'}
ignored_exts = {'', '.pyc'}

ext_groups = {
  'source' : {
    'exts' : [
      '.ploy', '.iot',
      '.swift', '.swiftdeps', '.inc', '.dep', '.gyb', '.sil', '.apinotes', # swift.
      '.pch', '.h', '.hh', '.hpp', '.def', '.c', '.cc', '.cpp', '.m', '.mm', # C.
      '.ll', '.map', '.modulemap', '.exports', # llvm.
      '.py', '.cfg', # python.
      '.sh', '.bash', '.cmd', # shell.
      '.js', '.coffee', '.ts', # javascript.
      '.vert', '.frag', '.geom', '.shader', # shaders.
      '.ml', '.mli',
      '.hs',
      '.java', '.jsx', '.groovy',
      '.clj', '.elm', '.go', '.rb', '.pl', '.pm', '.php', '.vb', '.r', '.lua', '.bat', # others.
      '.el', '.vim', # editors.
      '.ini',
      '.cmake',
      '.diff', '.pat',
    ],
    # skip parentheses, brackets, braces, backlslash, empty comments, and whitespace.
    'blank_pattern' : r'^[\[\](){};\\#/*\t ]*$'
  },

  'text' : {
    'exts' : [
      '.txt', '.rtf',
      '.md', '.rst',
      '.wu',
    ],
    'blank_pattern' : r'^\s*$'
  },

  'data' : {
    'exts' : [
      '.json', '.jsons', '.jsonl', '.cson', '.yaml', '.yml',
      '.xml', '.plist', '.strings',
      '.html', '.css', '.header', '.footer', '.svg', '.less', '.scss',
      '.tmtheme', '.tmlanguage',
      '.sql',
    ],
    'blank_pattern' : r'^\s*$'
  },
}

opaque_source_dir_exts = [
  '.xcodeproj',
  '.xib',
]


exts_to_re = {}
for g in ext_groups.values():
  p = g.get('blank_pattern')
  r = re.compile(p) if p else None
  for e in g['exts']:
    assert e not in exts_to_re
    exts_to_re[e] = r

# print order.
ext_group_keys = ['source', 'text', 'data']


def path_ext(path):
  return split_ext(path)[1].lower()

def ignore_dir_name(name):
  # note: takes name, not path.
  return name != '.' and name.startswith('.') or path_ext(name) in opaque_source_dir_exts


def main():
  arg_parser = ArgumentParser(description='Count lines of source code.')
  arg_parser.add_argument('paths', nargs='+', help='Directories to explore.')
  args = arg_parser.parse_args()

  files = Counter()
  lines = Counter()
  blank = Counter()
  other_exts = Counter()

  # iterate over all paths.
  for top in args.paths:
    if ignore_dir_name(path_name(top)): continue
    for dirpath, dirnames, filenames in os.walk(top):
      # filter dirnames.
      dirnames[:] = [n for n in dirnames if not ignore_dir_name(n)]
      for name in filenames:
        ext = path_ext(name)
        if ext in ignored_exts:
          continue
        if ext not in exts_to_re:
          other_exts[ext] += 1
          continue
        files[ext] += 1
        r = exts_to_re[ext]
        if not r:
          continue
        path = path_join(dirpath, name)
        try:
          with open(path) as f:
            for line in f:
              if r.match(line):
                blank[ext] += 1
              else:
                lines[ext] += 1
        except (IOError, UnicodeDecodeError) as e:
          print('skipping ({}): {}'.format(e, path), file=stderr)

  for k in ext_group_keys:
    g = ext_groups[k]
    non_zero = False
    total_key = k.upper() + ' TOTAL'
    # tricky: count values for total_key as we go, then print values for total_key last.
    sorted_keys = sorted(g['exts'], key=lambda k: lines[k])
    for e in sorted_keys + [total_key]:
      f = files[e]
      if f < 1:
        continue
      non_zero = True
      print('{:>12}: {:>5}  '.format(e, f), end='')
      files[total_key] += f
      if e in lines:
        l = lines[e]
        b = blank[e]
        t = l + b
        frac = float(l / t) if t > 0 else 0.0
        print(' {:>12,} lines; {:>12,} ({:.2f}) full'.format(t, l, frac), end='')
        lines[total_key] += l
        blank[total_key] += b
      print()
    if non_zero:
      print()

  if other_exts:
    items = sorted(other_exts.items(), key=lambda i: (-i[1], i[0]))
    print('; '.join('{}: {}'.format(ext, count) for (ext, count) in items))


if __name__ == '__main__': main()
