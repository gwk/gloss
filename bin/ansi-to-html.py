#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

'''
Convert ansi graphic rendition terminal escape codes to css-html.
http://en.wikipedia.org/wiki/ANSI_escape_code.
'''

#control sequence initiator (CSI): '\x1B['
#select graphic rendition (SGR) suffix: 'm'

import html
import re
from sys import stderr, argv, stdin


# scan for control sequence terminated by SGR, capturing semicolon-separated numeric codes
cs_re = re.compile('\x1B' + r'\[((?:\d+;?)*)m')

# supported ansi code features

# map ansi codes to css classes
# this will be filled out with color and background color classes below
codes_to_classes = {
  1 : 'bold',
  4 : 'underline',
  5 : 'blink',
}

# ansi attribute reset codes
reset_codes_to_classes = {
  22 : 'bold',
  24 : 'underline',
  25 : 'blink',
  39 : 'color',
  49 : 'bg-color',
}

codes_to_classes.update(reset_codes_to_classes)
reset_codes = frozenset(reset_codes_to_classes)

# ansi codes to (gloss color key, css color name) pairs
color_codes_to_pairs = {
  30 : ('k', 'black'),
  31 : ('r', 'red'),
  32 : ('g', 'green'),
  33 : ('y', 'yellow'),
  34 : ('b', 'blue'),
  35 : ('p', 'purple'),
  36 : ('c', 'cyan'),
  37 : ('l', 'lightgray'),
}

print('''\
<html>
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <style text="text/css">
    body { color: white; background: #181818; }
    pre {
      background: black;
      font-family: Source Code Pro, Menlo, Terminal, monospace;
      font-size: 11;
    }
    span.ansi-bold         { font-weight: bold; }
    span.ansi-underline    { text-decoration: underline; }
    span.ansi-blink        { text-decoration: blink; }''')

bg_css = []
for color_code, (key, css_color) in color_codes_to_pairs.items():
  class_ = 'color-' + key
  bg_class = 'bg-' + class_
  codes_to_classes[color_code] = class_
  codes_to_classes[color_code + 10] = bg_class
  print('      span.ansi-{:10} {{ color: {}; }}'.format(class_, css_color))
  bg_css.append('      span.ansi-{:10} {{ background-color: {}; }}'.format(bg_class, css_color))

print(*bg_css, sep='\n')

print('''\
  </style>
</head>
<body>''')

# a list of all the open span classes
class_stack = []

def open_span(class_):
  print('<span class="ansi-{}">'.format(class_), end='')

def close_span():
  print('</span>', end='')

def open_span_push(class_):
  #errSLD('open_span_push:', class_stack, class_)
  open_span(class_)
  class_stack.append(class_)

def close_spans_clear():
  #errSLD('close_spans_clear:', class_stack)
  for i in class_stack:
    close_span()
  del class_stack[:]


def excise_span_if_present(class_):
  #errFLD('excise: {}; {}', class_stack, class_)
  excise_index = None
  for i, c in enumerate(class_stack):
    if excise_index is not None: # target class already found
      assert not c.startswith(class_[:2]), f'found subsequent class: {c}; after excising target class: {class_}'
      open_span(c) # reopen remaining span
    elif c.startswith(class_[:2]):
      excise_index = i
      for i in range(i, len(class_stack)):
        close_span() # close all remaining spans, including this one
  #errSLD('excise index:', excise_index)
  if excise_index is not None:
    del class_stack[excise_index]


# returns the end position for the scanned section
def scan_section(line, pos):
  m = cs_re.search(line, pos)
  if not m: # no match; done
    print(html.escape(line[pos:], quote=False), end='')
    return len(line)
  # output up to the csi
  print(html.escape(line[pos:m.start()], quote=False), end='')
  code_string = m.group(1)
  codes = []
  for s in code_string.split(';'):
    if not s: continue # splitting empty string returns empty string
    try:
      code = int(s)
    except ValueError:
      print(f'ERROR: could not parse code: {s!r}; sequence: {code_string!r}', file=stderr)
      continue
    codes.append(code)
  #errSLD('codes:', codes)
  if not codes: # empty sequence is equivalent to a clear
    close_spans_clear()
  for code in codes:
    if code == 0: # reset
      close_spans_clear()
      continue
    try:
      class_ = codes_to_classes[code]
    except KeyError:
      print('NOTICE: unrecognized SGR code:', code, file=stderr)
      continue
    excise_span_if_present(class_)
    if code not in reset_codes:
      open_span_push(class_)
  return m.end()


def scan_file(f):
  print('<pre>')
  for line in f:
    pos = 0
    while pos < len(line):
      pos = scan_section(line, pos)
  close_spans_clear()
  print('\n</pre>')


# main
l  = len(argv)
if l == 1:
  scan_file(stdin)
elif l == 2:
  with open(argv[1]) as f:
    scan_file(f)
else:
  for path in argv[1:]:
    print('<br/><h3>{}</h3>'.format(html.escape(path, quote=False)))
    with open(path) as f:
      scan_file(f)
print('</body>\n</html>')
