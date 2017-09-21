#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

'''
Generate the gloss-black theme.
'''

import json
import re
from sys import argv


def main():
  theme = {
    'name': 'gloss-black',
    'settings' : make_settings()
  }
  with open(argv[1], 'w') as f:
    json.dump(theme, f, indent=2)


def make_settings():
  all_settings = []

  def base(**settings):
    validate(settings)
    all_settings.append({'settings': settings})

  def scope(*scopes, **settings):
    validate(settings)
    all_settings.append({'scope': scopes, 'settings': settings})

  base(
    activeGuide=D2,
    background=K,
    bracketsForeground=Y,
    bracketsOptions=['underline'],
    bracketContentsForeground=W,
    bracketContentsOptions=['underline'],
    caret=L1,
    findHighlight=C,
    findHighlightForeground=N,
    foreground=W,
    invisibles=D3,
    lineHighlight=D1,
    selection=L6,
    selectionBorder=L5,
    tagsOptions=['stippled_underline'],
  )

  scope('comment', foreground=N)
  scope('comment.punctuation', foreground=N)

  scope('constant', foreground=Az)

  scope('entity', foreground=Ch)

  scope('invalid', background=R)
  scope('invalid.deprecated', background='#800000')

  scope('keyword', foreground=M)
  scope('keyword.operator', foreground=MVi)

  scope('markup', foreground=Vi)
  scope('markup.deleted', foreground=R)
  scope('markup.inserted', foreground=G)
  scope('markup.changed', foreground=Vi)

  scope('message', foreground=Or)
  scope('message.error', foreground=Ro)

  scope('meta', foreground=W) # too broad.
  scope('meta.diff, meta.diff.header', foreground=R)

  scope('punctuation', foreground=L2)

  scope('storage', foreground=Y)
  scope('storage.type', fontStyle='italic')

  scope('string', foreground=YOr)
  scope('string punctuation', foreground=Y)

  scope('support', foreground=G)

  scope('variable', foreground=Ro)

  scope('sym', foreground=G)

  # legs.
  scope('sym.legs', foreground=W)
  scope('section.legs', foreground=L4)
  scope('section_invalid.legs', foreground=L4, background='#800000')

  scope('colon.legs', foreground=C)
  scope('brckt_o', foreground=C)
  scope('brckt_c', foreground=C)
  scope('brace_o', foreground=C)
  scope('brace_c', foreground=C)
  scope('paren_o', foreground=C)
  scope('paren_c', foreground=C)
  scope('bar', foreground=C)
  scope('qmark', foreground=C)
  scope('star', foreground=C)
  scope('plus', foreground=C)
  scope('amp', foreground=C)
  scope('dash', foreground=C)
  scope('caret', foreground=C)
  scope('ref', foreground=G)
  scope('esc', foreground=B)
  scope('char', foreground=W)


  return all_settings


# colors.
# one possible future abbreviation scheme:
#   mixtures with white are called tints; mixtures with black are shades.
K = '#000000' # black.
D1 = '#101010' # dark.
D2 = '#202020'
D3 = '#303030'
D4 = '#404040'
D5 = '#505050'
D6 = '#606060'
D7 = '#707070'
N = '#808080' # neutral gray; not present in ANSI SGR codes.
L7 = '#909090'
L6 = '#A0A0A0'
L5 = '#B0B0B0'
L4 = '#C0C0C0'
L3 = '#D0D0D0'
L2 = '#E0E0E0'
L1 = '#F0F0F0'
W = '#FFFFFF' # white.

R = '#FF0000'
G = '#00FF00'
B = '#0000FF'

Y = '#FFFF00'
C = '#00FFFF'
M = '#FF00FF'

Or = '#FF8000' # orange.
Ch = '#80FF00' # chartreuse.
Sp = '#00FF80' # spring green.
Az = '#0080FF' # azure.
Vi = '#8000FF' # violet.
Ro = '#FF0080' # rose.

RRo = '#FF0040'
ROr = '#FF4000'
YOr = '#FFC000'
YCh = '#C0FF00'
GCh = '#40FF00'
GSp = '#00FF40'
CSp = '#00FFC0'
CAz = '#00C0FF'
BAz = '#0040FF'
BVi = '#4000FF'
MVi = '#C000FF'
MRo = '#FF00C0'

# TODO: valid keys.

valid_words = { 'bold', 'italic', 'underline', 'stippled_underline' }

def validate_value(v):
  if v is None: return
  if isinstance(v, str):
    if v.isdigit(): return
    if v.startswith('#'):
      if not re.fullmatch('#[0-9A-F]{6}', v):
        raise ValueError('bad hex value: {}'.format(v))
      return
    words = v.split()
    for w in words:
      if not w in valid_words:
        raise ValueError('validate encountered bad word: {}'.format(w))
  elif isinstance(v, list):
    for el in v:
      validate_value(el)
  else:
    raise ValueError('bad type: {}'.format(v))

def validate(d):
  for k, v in d.items():
    # TODO: validate keys. raise KeyError(k)
    validate_value(v)


if __name__ == '__main__': main()
