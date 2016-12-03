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

groups = {
  'source' : {
    'exts' : [
      '.ploy',
      '.swift', '.swiftdeps', '.inc', '.dep', '.gyb', '.sil', '.apinotes', # swift.
      '.pch', '.h', '.hh', '.hpp', '.def', '.c', '.cc', '.cpp', '.m', '.mm', # C.
      '.ll', '.map', '.modulemap', '.exports', # llvm.
      '.py', '.cfg', # python.
      '.rs', '.rc', '.rust',
      '.sh', '.bash', '.cmd', # shell.
      '.js', '.coffee', '.ts', # javascript.
      '.vert', '.frag', '.geom', '.shader', # shaders.
      '.ml', '.mli',
      '.hs',
      '.java', '.jsx', '.groovy',
      '.clj', '.elm', '.go', '.rb', '.pl', '.pm', '.php', '.vb', '.r', '.lua', '.bat', # others.
      '.el', '.vim', # editors.
      '.ini',
      '.cmake', '.mk', '.in', '.ac', '.am', '.m4',
      '.diff', '.pat',
      '.awk',
      '.l', '.y', '.g4',
    ],
    # skip parentheses, brackets, braces, backlslash, empty comments, and whitespace.
    'blank_pattern' : r'[\[\](){};\\#/*\s]*'
  },

  'test' : {
    'exts': [
      '.iot',
      '.err', '.out',
      '.stderr', '.stdout',
    ],
    'blank_pattern' : r'\s*',
  },

  'text' : {
    'exts' : [
      '.txt', '.rtf',
      '.md', '.rst',
      '.wu',
    ],
    'blank_pattern' : r'\s*',
  },

  'data' : {
    'exts' : [
      '.dot',
      '.json', '.jsons', '.jsonl', '.cson', '.yaml', '.yml', '.toml',
      '.xml', '.plist', '.strings',
      '.html', '.css', '.header', '.footer', '.svg', '.less', '.scss',
      '.tmtheme', '.tmlanguage',
      '.sql',
      '.1', '.2', '.3', '.4', '.5', '.6', '.7', '.8',
    ],
    'blank_pattern' : r'\s*$',
  },
}

opaque_source_dir_exts = [
  '.xcodeproj',
  '.xib',
]


# print order.
group_keys = ['source', 'test', 'text', 'data']


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
        path = path_join(dirpath, name)
        try:
          with open(path) as f:
            for line in f:
              if r.fullmatch(line):
                blank[ext] += 1
              else:
                lines[ext] += 1
        except (IOError, UnicodeDecodeError) as e:
          print('skipping ({}): {}'.format(e, path), file=stderr)

  for group_key in group_keys:
    group = groups[group_key]
    non_zero = False
    total_key = group_key.upper() + ' TOTAL'
    sorted_keys = sorted(group['exts'], key=lambda k: lines[k]) # sort by substantial line count.
    # tricky: count values for total_key as we go, then print values for total_key last.
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


def path_ext(path):
  return split_ext(path)[1].lower()

def ignore_dir_name(name):
  # note: takes name, not path.
  return name != '.' and name.startswith('.') or path_ext(name) in opaque_source_dir_exts


exts_to_re = {}
for g in groups.values():
  pattern = g['blank_pattern']
  r = re.compile(pattern)
  for e in g['exts']:
    if e in exts_to_re: raise ValueError(e)
    exts_to_re[e] = r


if __name__ == '__main__': main()
