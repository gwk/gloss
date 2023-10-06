#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import signal
import shlex

from os.path import isdir as is_dir, isfile as is_file
from subprocess import PIPE, Popen
from sys import stderr
from typing import Any, NoReturn


def run(cmd:str, exp:int|None=None) -> tuple[int, str, str]:
  cmd_words = shlex.split(cmd)
  proc = Popen(cmd_words, stdin=None, stdout=PIPE, stderr=PIPE, shell=False)
  p_out, p_err = proc.communicate() # waits for process to complete.
  code = proc.returncode
  if exp is not None and code != exp:
    raise ValueError('bad subprocess exit code', cmd, exp, code, p_err)
  return code, p_out.decode('utf-8'), p_err.decode('utf-8')


def runC(cmd:str) -> int:
  'Run a command and return exit code.'
  c, o, e = run(cmd=cmd, exp=None)
  return c


def runCO(cmd:str) -> tuple[int,str]:
  'Run a command and return exit code, std out; optional err.'
  c, o, e = run(cmd=cmd, exp=None)
  return c, o


def runO(cmd:str, exp=0) -> str:
  'Run a command and return exit code, std out; optional err.'
  c, o, e = run(cmd=cmd, exp=exp)
  return o



# because a long prompt calculation is debilitating, set a single global timeout for the process.
time_limit = 1

def prompt(*items:Any) -> NoReturn:
  print(*items, ' ', sep='', end='')
  exit(0)

def alarm_handler(signum, current_stack_frame):
  prompt('<TIMEOUT>')

signal.signal(signal.SIGALRM, alarm_handler) # set handler.
signal.alarm(time_limit) # set alarm.

try:
  c, gdo = runCO('git rev-parse --git-dir')
  if c != 0: # not a git dir.
    exit(0)

  # current git dir.
  gd = gdo.strip()
  # we currently do not respect svn-remotes; can be determined with this command.
  #git config -z --get-regexp '^(svn-remote\..*\.url)$'

  if runO('git rev-parse --is-bare-repository') == 'true\n':
    bare_prefix = 'BARE:'
  elif runO('git rev-parse --is-inside-git-dir') == 'true\n':
    prompt('.GIT')
  else:
    bare_prefix = ''


  def find_branch() -> tuple[str,str]:
    'Returns a pair: branch string (needs to be stripped) and mode suffix.'
    if is_file(gd + '/rebase-merge/interactive'):
      return open(gd + '/rebase-merge/head-name').read(), '|REBASE-i'
    if is_dir(gd + '/rebase-merge'):
      return open(gd + '/rebase-merge/head-name').read(), '|REBASE-m'

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

    c, b = runCO('git symbolic-ref HEAD')
    if c == 0:
      return b, s
    # detached.
    c, b = runCO('git describe --contains --all HEAD')
    if c == 0:
      return b, s
    # last option.
    try: head_sha = open(gd + '/HEAD').read()[:8]
    except FileNotFoundError: head_sha = 'unknown'
    return f'({head_sha})', s


  branch_path_n, suffix = find_branch()
  branch_path = branch_path_n.strip()
  branch_name = branch_path
  for prefix in ['refs/heads/', 'remotes/']:
    if  branch_name.startswith(prefix):
      branch_name = branch_name[len(prefix):]
      break


  w = '' # working.
  i = '' # index (staged).
  s = '' # stash.
  u = '' # unknown.

  if runO('git rev-parse --is-inside-work-tree') == 'true\n':
    if runC('git diff --no-ext-diff --quiet --exit-code') != 0:
      w = '*'
    if runC('git rev-parse --quiet --verify HEAD') == 0: # verify that HEAD is valid.
      if runC('git diff-index --cached --quiet HEAD'):
        i ='+'
    else: # head is not valid.
      i = '#'
  if runC('git rev-parse --verify refs/stash') == 0:
    s='$'
  if runO('git ls-files --others --exclude-standard'):
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
