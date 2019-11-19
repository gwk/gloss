#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

'''
Generate the gloss-black theme.

for settings color customizations, see https://code.visualstudio.com/docs/getstarted/theme-color-reference.
'''

import json
import re
from sys import argv

from pithy.fs import make_dirs
from pithy.path import path_dir


def main():
  out_path = argv[1]
  out_dir = path_dir(out_path)
  make_dirs(out_dir)

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
  scope('constant.language', foreground=Az)
  scope('constant.numeric', foreground=Az)

  scope('entity', foreground=Ch)

  scope('invalid', foreground='#800000')
  scope('invalid.deprecated', foreground=RD)

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

  scope('punctuation', foreground=C)

  scope('storage', foreground=Y)
  scope('storage.type', fontStyle='italic')

  scope('string', foreground=YOr)
  scope('string punctuation', foreground=Y)

  scope('support', foreground=G)

  scope('variable', foreground=Ro)

  scope('sym', foreground=G)

  scope('comment.typehint', foreground=L4)



  # Python.
  # All scopes: https://raw.githubusercontent.com/MagicStack/MagicPython/master/misc/scopes.
  # Syntax source: https://github.com/MagicStack/MagicPython/tree/master/grammars/src.
  scope('constant.other.caps.python', foreground=W)
  scope('constant.other.ellipsis.python', foreground=Vi)
  scope('entity.name.function.decorator.python', foreground=G)
  scope('keyword.illegal.name.python', foreground=R8)
  scope('meta.format.brace.python', foreground=R) # TODO: debug.
  scope('support.function.builtin.python', foreground=W)
  scope('support.variable.magic.python', foreground=Sp)
  scope('variable.legacy.builtin.python', foreground=W)

  # Python strings.
  scope('constant.character.escape.python', foreground=Or)
  scope('constant.character.format.placeholder.other.python', foreground=G) # Brace in f-string.
  scope('storage.type.format.python', foreground=BVi) # Brace format starting at colon.

  # Regexp.
  scope('constant.character.set.regexp', foreground=G)
  scope('constant.character.escape.regexp', foreground=Or)
  scope('constant.other.set.regexp', foreground=C) # Square brackets.

  scope('entity.name.tag.backreference.regexp', foreground=Ro)
  scope('entity.name.tag.named.backreference.regexp', foreground=Ro)

  scope('entity.name.tag.named.group.regexp', foreground=B) # `?P<name>`.
  scope('storage.modifier.flag.regexp', foreground=ROr) # `(?x)`.
  scope('support.other.escape.special.regexp', foreground=Or) # `\w`.
  scope('constant.character.unicode.regexp', foreground=Or)

  # Legs.

  scope('sym.legs', foreground=W)
  scope('section.legs', foreground=L4)
  scope('section_invalid.legs', foreground=R)

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


  # Writeup.
  scope('entity.section.writeup', foreground=C)
  scope('entity.code.writeup', foreground=L4)
  scope('meta.version.writeup', foreground=D4)
  return all_settings


# colors.
# one possible future abbreviation scheme:
#   mixtures with white are called tints; mixtures with black are shades.
K  = '#000000' # black.
D1 = '#101010' # dark.
D2 = '#202020'
D3 = '#303030'
D4 = '#404040'
D5 = '#505050'
D6 = '#606060'
D7 = '#707070'
N  = '#808080' # neutral gray; not present in ANSI SGR codes.
L7 = '#909090'
L6 = '#A0A0A0'
L5 = '#B0B0B0'
L4 = '#C0C0C0'
L3 = '#D0D0D0'
L2 = '#E0E0E0'
L1 = '#F0F0F0'
W  = '#FFFFFF' # white.

R  = '#FF0000'
R8 = '#800000'
RD = '#D00000'
G  = '#20FF20'
B  = '#6060FF' # Lighten.

Y = '#FFFF00'
C = '#00FFFF'
M = '#FF00FF'

Or = '#FF8000' # orange.
Ch = '#80FF00' # chartreuse.
Sp = '#00FF80' # spring green.
Az = '#1080FF' # azure. Lightened.
Vi = '#8010FF' # violet. Lightened.
Ro = '#FF0080' # rose.

RRo = '#FF0040'
ROr = '#FF4000'
YOr = '#FFC000'
YCh = '#C0FF00'
GCh = '#40FF00'
GSp = '#00FF40'
CSp = '#00FFC0'
CAz = '#00C0FF'
BAz = '#2040FF' # Lightened.
BVi = '#6020FF' # Lightened.
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
