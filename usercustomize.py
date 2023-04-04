import re
import os
import sys
import pathlib

from types import TracebackType
from typing import Type


def gloss_excepthook(type_:Type[BaseException], value:BaseException, traceback:TracebackType) -> None:

  from traceback import format_exception
  stderr = sys.stderr

  def sgr(*codes) -> str:
    'Select Graphic Rendition control sequence string.'
    code = ';'.join(str(c) for c in codes)
    return '\x1b[{}m'.format(code)

  RST = sgr()
  RST_TXT = sgr(38, 0)

  # xterm-256 sequence initiators; these should be followed by a single color index.
  # Both text and background can be specified in a single sgr call.
  TXT = '38;5'
  BG = '48;5'

  # RGB6 color cube: 6x6x6, from black to white.
  K = 16  # black.
  W = 231 # white.

  def gray26(n:int) -> int:
    assert 0 <= n < 26
    if n == 0: return K
    if n == 25: return W
    return W + n

  def rgb6(r:int, g:int, b:int) -> int:
    'index RGB triples into the 256-color palette (returns 16 for black, 231 for white).'
    assert 0 <= r < 6
    assert 0 <= g < 6
    assert 0 <= b < 6
    return (((r * 6) + g) * 6) + b + 16

  TXT_R3 = sgr(TXT, rgb6(3,0,0))
  TXT_D = sgr(TXT, gray26(9))
  TXT_N = sgr(TXT, gray26(13))
  TXT_L = sgr(TXT, gray26(16))
  TXT_G = sgr(TXT, rgb6(0, 4, 0))
  TXT_O = sgr(TXT, rgb6(5, 2, 0))
  TXT_Y = sgr(TXT, rgb6(5, 5, 0))

  stderr.write('\n') # Add a newline before the traceback in case the last line was not terminated.
  messages = format_exception(type_, value, traceback, limit=None, chain=True)
  for msg in messages:
    m = _exc_msg_re.fullmatch(msg)
    if not m:
      stderr.write(msg)
      continue
    k = m.lastgroup
    if k == 'traceback':
      stderr.write(f'{TXT_R3}{m[0]}{RST}\n')
    elif k == 'stack_frame':
      file = m['stack_file']
      line = m['stack_line']
      s_in = ' in ' if m['stack_in'] else ''
      fn = m['stack_fn']
      code = m['stack_code']
      if file.startswith(_starting_work_dir_slash):
        rel_file = file[len(_starting_work_dir_slash):]
        file = ('' if ('/' in rel_file) else './') + rel_file
      elif file.startswith(_home_dir_slash):
        rel_file = file[len(_home_dir_slash):]
        file = '~/' + rel_file
      stderr.write(f'{TXT_L}  {file}:{line}{TXT_D}{s_in}{TXT_G}{fn}{RST}{code}')
      #stderr.write(repr(msg)+'\n')
    elif k == 'recursion':
      stderr.write(f'{TXT_R3}{m[0]}{RST}')
    elif k == 'exception':
      name = m['exc_name']
      msg = m['exc_msg']
      stderr.write(f'{TXT_O}{name}{RST}{TXT_Y}{msg}{RST}\n')
    else:
      stderr.write(repr(msg)+'\n')


_home_dir = str(pathlib.Path.home())
_home_dir_slash = _home_dir + ('' if _home_dir.endswith('/') else '/')

_work_dir = os.getcwd()
_starting_work_dir_slash = _work_dir + ('' if _work_dir.endswith('/') else '/')



# Classify and dissect each message from format_exception.
# Each message should have one (or more?) newlines.
_exc_msg_re = re.compile(r'''(?sx) # s=Dotall; allows matching of newlines in trailing content.
  (?P<traceback>Traceback\ \(most\ recent\ call\ last\):\n )
| (?P<stack_frame>\ \ File\ "(?P<stack_file>[^"\n]+)",\ line\ (?P<stack_line>\d+)(?P<stack_in>,\ in\ )?(?P<stack_fn>[^\n]+)
    (?P<stack_code>.*) )
| (?P<recursion>\ \ \[Previous\ line\ repeated\ [^\n\]]+\]\n )
| (?P<exception> (?P<exc_name>[.\w]+:?) (?P<exc_msg>.*) )
''')

sys.excepthook = gloss_excepthook
