#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import sys
from argparse import ArgumentParser
from cProfile import Profile
from pstats import Stats
from os.path import dirname


def main():
  parser = ArgumentParser(description="Run a python script under Python's cProfile profiler.")
  parser.add_argument('-sort', nargs='+', default=['cumulative', 'filename', 'name'], help='sort keys')
  parser.add_argument('-filter', nargs='+', default=[], help='filtering clauses')
  parser.add_argument('cmd', nargs='+', help='the command to run')
  args = parser.parse_args()

  cmd = args.cmd
  cmd_path = cmd[0]

  def filter_clause(word):
    for T in (int, float):
      try: return T(word)
      except ValueError: pass
    return word

  filter_clauses = [filter_clause(word) for word in args.filter]

  with open(cmd_path, 'rb') as f:
    code = compile(f.read(), cmd_path, 'exec')

  globals_ = {
    '__file__': cmd_path,
    '__name__': '__main__',
    '__package__': None,
    '__cached__': None,
  }

  sys.argv[:] = cmd
  # also need to fix the search path to imitate the regular interpreter.
  sys.path[0] = dirname(cmd_path) # not sure if this is right in all cases.

  profile = Profile()
  exit_code = 0
  try:
    profile.runctx(code, globals=globals_, locals=None)
  except SystemExit as e:
    exit_code = e.code
  except BaseException:
    from traceback import TracebackException
    exit_code = 1 # exit code that Python returns when an exception raises to toplevel.
    # Format the traceback as it would appear when run standalone.
    traceback = TracebackException(*sys.exc_info())
    # note: the traceback will contain stack frames from the host.
    # this can be avoided with a fixup function, but does not seem necessary at this point. See coven.py for an example.
    #fixup_traceback(traceback)
    print(*traceback.format(), sep='', end='', file=sys.stderr)

  print('\n', '=' * 64, sep='')

  stats = Stats(profile)
  stats.sort_stats(*args.sort)
  stats.print_stats(*filter_clauses)
  # TODO: enter into an interactive mode?
  # TODO: support print_callers, print_callees.


main()

'''
'calls'	call count
'cumulative'	cumulative time
'cumtime'	cumulative time
'file'	file name
'filename'	file name
'module'	file name
'ncalls'	call count
'pcalls'	primitive call count
'line'	line number
'name'	function name
'nfl'	name/file/line
'stdname'	standard name
'time'	internal time
'tottime'	internal time
'''
