#!/usr/bin/env python3
# Copyright 2013 George King. Permission to use this file is granted in license-gloss.txt.

import signal

from pithy.io import read_from_path
from pithy.fs import is_dir, is_file 
from pithy.task import dev_null, runC, runCO, runO
from pithy.strings import clip_first_prefix


# because a long prompt calculation is debilitating, set a single global timeout for the process.
time_limit = 1

def prompt(*items):
  print(' ', *items, sep='', end='')
  exit(0)

def alarm_handler(signum, current_stack_frame):
  prompt('GIT TIMEOUT')

signal.signal(signal.SIGALRM, alarm_handler) # set handler.
signal.alarm(time_limit) # set alarm.

try:
  null = dev_null()
  c, gdo = runCO('git rev-parse --git-dir', err=null)
  if c != 0: # not a git dir.
    exit(0)

  # current git dir.
  gd = gdo.strip()
  # we currently do not respect svn-remotes; can be determined with this command.
  #git config -z --get-regexp '^(svn-remote\..*\.url)$'

  if runO('git rev-parse --is-bare-repository', exp=0) == 'true\n':
    bare_prefix = 'BARE:'
  elif runO('git rev-parse --is-inside-git-dir', exp=0) == 'true\n':
    prompt('.GIT')
  else:
    bare_prefix = ''


  def find_branch():
    'returns  a pair: branch string (needs to be stripped) and mode suffix.'
    if is_file(gd + '/rebase-merge/interactive'):
      return read_from_path(gd + '/rebase-merge/head-name'), '|REBASE-i'
    if is_dir(gd + '/rebase-merge'):
      return read_from_path(gd + '/rebase-merge/head-name'), '|REBASE-m'

    # determine suffix first.
    if is_dir(gd + '/rebase-apply'):
      if is_file(gd + '/rebase-apply/rebasing'):
        s = '|REBASE'
      elif is_file(gd + '/rebase-apply/applying'):
        s = '|AM'
      else:
        s = '|AM/REBASE'
    elif is_file(gd + '/MERGE_HEAD'):
      s = '|MERGE'
    elif is_file(gd + '/CHERRY_PICK_HEAD'):
      s = '|CHERRY-PICK'
    elif is_file(gd + '/BISECT_LOG'):
      s = '|BISECT'
    else:
      s = ''

    c, b = runCO('git symbolic-ref HEAD', err=null)
    if c == 0:
      return b, s
    # detached.
    c, b = runCO('git describe --contains --all HEAD', err=null)
    if c == 0:
      return b, s
    # last option.
    head_sha = read_from_path(gd + '/HEAD', default='unknown')
    return '({})'.format(head_sha[:8]), s


  branch_path_n, suffix = find_branch()
  branch_path = branch_path_n.strip()
  branch_name = clip_first_prefix(branch_path, ['refs/heads/', 'remotes/'], req=False)

  w = '' # working.
  i = '' # index (staged).
  s = '' # stash.
  u = '' # unknown.

  if runO('git rev-parse --is-inside-work-tree', exp=0) == 'true\n':
    if runC('git diff --no-ext-diff --quiet --exit-code', out=null) != 0:
      w = '*'
    if runC('git rev-parse --quiet --verify HEAD', out=null) == 0: # verify that HEAD is valid.
      if runC('git diff-index --cached --quiet HEAD', out=null):
        i ='+'
    else: # head is not valid.
      i = '#'
  if runC('git rev-parse --verify refs/stash', out=null, err=null) == 0:
    s='$'
  if runO('git ls-files --others --exclude-standard', exp=0):
    u='%'

  # position.
  c, count_str = runCO('git rev-list --count --left-right "@{upstream}"...HEAD')
  if c: # error; assume no upstream configured.
    pos = '^'
  else:
    rem, tab, loc = count_str.strip().partition('\t')
    if rem != '0':
      if loc != '0':
        pos = '<>'
      else:
        pos = '<'
    else:
      if loc != '0':
        pos = '>'
      else:
        pos = '='

  prompt(bare_prefix, branch_name, w, i, s, u, suffix, pos)

except Exception:
  print(' GIT ERROR', end='') # this will show up in the command prompt.
  raise
