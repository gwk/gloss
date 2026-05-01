#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import shlex
import signal
from os.path import isdir as is_dir, isfile as is_file
from subprocess import PIPE, Popen
from typing import Any, NoReturn


def run(cmd:str, exp:int|None=None) -> tuple[int,str,str]:
  'Run a command and return exit code, std out; optional err.'
  cmd_words = shlex.split(cmd)
  proc = Popen(cmd_words, stdin=None, stdout=PIPE, stderr=PIPE, shell=False)
  p_out, p_err = proc.communicate()
  code = proc.returncode
  if exp is not None and code != exp:
    raise ValueError('bad subprocess exit code', cmd, exp, code, p_err)
  return code, p_out.decode('utf-8'), p_err.decode('utf-8')


def runCO(cmd:str) -> tuple[int,str]:
  'Run a command and return exit code, std out.'
  c, o, _e = run(cmd=cmd, exp=None)
  return c, o


def runO(cmd:str, exp=0) -> str:
  'Run a command and return std out.'
  c, o, _e = run(cmd=cmd, exp=exp)
  return o


def prompt(*items:Any) -> NoReturn:
  'Print the prompt string and exit.'
  print(*items, sep='', end=' ')
  exit(0)


def prefix(prefix:str, *items:str) -> str:
  joined = ''.join(items)
  return (prefix + joined) if joined else ''

# Because a long prompt calculation is debilitating, set a single global timeout for the process.
time_limit = 1

def alarm_handler(signum, current_stack_frame):
  prompt('<TIMEOUT>')

signal.signal(signal.SIGALRM, alarm_handler)
signal.alarm(time_limit)


def worktree_prompt() -> None:
  c, gd_raw = runCO('git rev-parse --git-dir')
  if c != 0: exit() # Not a git dir. do not print anything.

  gd = gd_raw.strip()

  if runO('git rev-parse --is-inside-git-dir') == 'true\n':
    prompt('.GIT')

  if runO('git rev-parse --is-bare-repository') == 'true\n':
    prompt('bare')

  status_out = runO('git status --porcelain=v2 --branch --show-stash')

  headers:dict[str,str] = {}
  status_lines:list[tuple[str,...]] = []
  for line in status_out.splitlines():
    if line.startswith('# '): # Header.
      key, _, val = line[2:].partition(' ')
      headers[key] = val
    else:
      status_lines.append(tuple(line.split(' ')))


  # branch.oid <commit> | (initial)   # Current commit.
  # branch.head <branch> | (detached) # Current branch.
  # branch.upstream <upstream-branch> # If upstream is set.
  # branch.ab +<ahead> -<behind>      # If upstream is set and the commit is present.
  # Stash <N>                         # Number of stashed changes.
  branch_oid = headers.get('branch.oid', '')
  branch_head = headers.get('branch.head', '')
  branch_upstream = headers.get('branch.upstream', '')

  ab_counts = ''
  if branch_upstream:
    if branch_ab := headers.get('branch.ab', ''):
      branch_ahead_str, _, branch_behind_str = branch_ab.partition(' ')
      branch_ahead = int(branch_ahead_str.lstrip('+'))
      branch_behind = int(branch_behind_str.lstrip('-'))
      if branch_ahead:
        ab_counts += f'+{branch_ahead}'
      if branch_behind:
        ab_counts += f'-{branch_behind}'
    if not ab_counts:
      ab_counts = '='

  stash_count = headers.get('stash', '')

  # 1 <XY> <sub> <mH> <mI> <mW> <hH> <hI> <path> # Ordinary changes.
  # 2 <XY> <sub> <mH> <mI> <mW> <hH> <hI> <X><score> <path><sep><origPath> # Renamed.
  # u <XY> <sub> <m1> <m2> <m3> <mW> <h1> <h2> <h3> <path> # Unmerged.
  # ? <path> # Untracked.
  # ! <path> # Ignored.

  # XY are (staged, unstaged) status symbols.
  # .: unchanged
  # M: modified
  # A: added
  # D: deleted

  index = ''
  working = ''
  unmerged = ''
  untracked = ''
  stash = f'${stash_count}' if stash_count else ''

  for line in status_lines:
    match line[0]:
      case '1'|'2':
        xy = line[1]
        x = xy[0]
        y = xy[1]
        if x != '.': index = '+'
        if y != '.': working = '*'
      case 'u':
        unmerged = '%'
      case '?':
        untracked = '?'
      case '!': pass
      case _: raise ValueError(f'Unexpected line: {line}')

  if branch_head == '(detached)':
    c2, desc = runCO('git describe --contains --all HEAD')
    branch_name = desc.strip() if c2 == 0 else f'({branch_oid[:8]})'
  else:
    branch_name = branch_head

  # Detect in-progress operations via filesystem; override branch name and add suffix.
  suffix = ''
  if is_file(gd + '/rebase-merge/interactive'):
    branch_name = open(gd + '/rebase-merge/head-name').read().strip()
    suffix = '|REBASE-i'
  elif is_dir(gd + '/rebase-merge'):
    branch_name = open(gd + '/rebase-merge/head-name').read().strip()
    suffix = '|REBASE-m'
  elif is_dir(gd + '/rebase-apply'):
    if is_file(gd + '/rebase-apply/rebasing'):
      suffix = '|REBASE'
    elif is_file(gd + '/rebase-apply/applying'):
      suffix = '|AM'
    else:
      suffix = '|AM/REBASE'
  elif is_file(gd + '/MERGE_HEAD'):
    suffix = '|MERGE'
  elif is_file(gd + '/CHERRY_PICK_HEAD'):
    suffix = '|CHERRY-PICK'
  elif is_file(gd + '/BISECT_LOG'):
    suffix = '|BISECT'

  # The rebase head-name is a full ref path; strip it.
  for pfx in ('refs/heads/', 'remotes/'):
    if branch_name.startswith(pfx):
      branch_name = branch_name[len(pfx):]
      break

  prompt(branch_name, ab_counts, stash, prefix(' ', index, working, unmerged, untracked), suffix)


try:
  worktree_prompt()
except Exception:
  print(' GIT ERROR', end='')
  raise
