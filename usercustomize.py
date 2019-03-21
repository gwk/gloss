import re
import os
import sys


def gloss_excepthook(exc_class:type, exc:BaseException, traceback) -> None:

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
  TXT_O = sgr(TXT, rgb6(5, 2, 0))
  TXT_Y = sgr(TXT, rgb6(5, 5, 0))

  lines = format_exception(exc_class, exc, traceback, limit=None, chain=True)
  for line in lines:
    m = _log_msg_re.match(line)
    if m:
      k = m.lastgroup
      if k == 'traceback':
        stderr.write(f'{TXT_R3}{m[0]}{RST}\n')
      elif k == 'stack_frame':
        f = m['stack_file']
        l = m['stack_line']
        fn = m['stack_fn']
        code = m['stack_code']
        stderr.write(f'{TXT_L}{f}:{l} {TXT_D}in {TXT_L}{fn}{RST_TXT}\n{code}')
      elif k == 'exception':
        name = m['exc_name']
        msg = m['exc_msg']
        if msg:
          stderr.write(f'{TXT_O}{name}{RST}: {TXT_Y}{msg}{RST}\n')
        else:
          stderr.write(f'{TXT_O}{name}{RST}\n')
      else:
        stderr.write(line)
    else:
      stderr.write(line)


_log_msg_re = re.compile(r'''(?x)
  (?P<traceback>Traceback \ \(most\ recent\ call\ last\): )
| (?P<stack_frame>\ \ File\ "(?P<stack_file>.+)",\ line\ (?P<stack_line>\d+),\ in\ (?P<stack_fn>.+)\n (?P<stack_code>.*\n?))
| (?P<exception> (?P<exc_name>[.\w]+) (?: :\ (?P<exc_msg>.+))?)
''')

sys.excepthook = gloss_excepthook
