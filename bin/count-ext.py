#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# count file extensions found in a directory tree.

# TODO:
# implement path arguments
# multiple arguments should cause each directory to be recursed
# stats should be printed for each directory when completed, then total stats when all done.

# implement ext listing (-l)
#  usage example: count-ext -l "mp3 m4a"
#  this would cause the relative path of each file matching the given extensions to be listed
#  in this case don't print stats, so that the results can be piped to other utilities


from argparse import ArgumentParser
import collections
import os
import os.path


def main():
  arg_parser = ArgumentParser(description='Count lines of source code.')
  arg_parser.add_argument('paths', nargs='+', help='Directories to explore.')
  args = arg_parser.parse_args()

  ext_counts = collections.defaultdict(int)

  for top in args.paths:
    for root, dirs, files in os.walk(top):
      for f in files:
        name, ext = os.path.splitext(f)
        ext_counts[ext] += 1

    empty_name = '[none]'
    max_len = max(len(empty_name), max(len(k) for k in ext_counts))

    for k in sorted(ext_counts.keys()):
      v = ext_counts[k]
      print('{0:{1}}: {2}'.format(k or empty_name, max_len, v))


if __name__ == '__main__': main()
