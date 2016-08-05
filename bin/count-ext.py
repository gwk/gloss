#!/usr/bin/env python3
# Copyright 2009 George King. Permission to use this file is granted in license-gloss.txt.

# count file extensions found in a directory tree.

# TODO:
# implement path arguments
# multiple arguments should cause each directory to be recursed
# stats should be printed for each directory when completed, then total stats when all done.

# implement ext listing (-l)
#  usage example: lsext -l "mp3 m4a" 
#  this would cause the relative path of each file matching the given extensions to be listed
#  in this case don't print stats, so that the results can be piped to other utilities


import os
import os.path
import optparse
import collections


# optparse
optparser = optparse.OptionParser(usage = 'usage: %prog')
(options, args) = optparser.parse_args()

if len(args) > 0:
  optparser.error('arguments not yet implemented')

path = "."

assert(os.path.isdir(path))

ext_counts = collections.defaultdict(int)

for root, dirs, files in os.walk(path):
  #   if files: print(root + ':') # could have a verbose mode that does this       
  for f in files:
    name, ext = os.path.splitext(f)
    ext_counts[ext] += 1

empty_name = '[none]'
max_len = max(len(empty_name), max(len(k) for k in ext_counts))

for k in sorted(ext_counts.keys()):
  v = ext_counts[k]
  if not k: k = empty_name
  print('{0:{1}}: {2}'.format(k, max_len, v))
