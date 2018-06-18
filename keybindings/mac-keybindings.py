#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

# https://developer.apple.com/library/mac/documentation/Cocoa/Conceptual/EventOverview/TextDefaultsBindings/TextDefaultsBindings.html.

import plistlib
import NSEventKeys
from pithy import errFL


def main():
  f = open('/System/Library/Frameworks/AppKit.framework/Resources/StandardKeyBinding.dict', 'rb')
  # note: user customizations go in '~/Library/KeyBindings/DefaultKeyBinding.dict'.
  bindings = plistlib.load(f)

  for key, cmd in sorted(bindings.items(), key=lambda p: repr(p[1])):
    if cmd == 'noop:': continue
    desc = '+'.join(translate_key(c) for c in key)
    errFL('{:<48} {!r}', str(cmd), desc)


def translate_key(c): return mods.get(c, c)

mods = {
  ' ' : 'space',
  '@' : 'cmd',
  '^' : 'ctrl',
  '~' : 'opt',
  '$' : 'shift',
  '#' : 'keypad', # does not translate correctly; should be joined with next character. currently not in defaults.
  '\x1b' : 'escape',
  '\x7f' : 'delete',
  '\x03' : 'endOfText',
  '\x08' : 'backspace',
  '\x19' : 'endOfMedium',
}

mods.update(NSEventKeys.keys)

main()
