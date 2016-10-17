#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.


'''
control pictures have the reserved range '\u2400' to '\u243F'.
the low 32 codes are offset from the control code they represent by 0x2400.
SP (space):   \u2420
DEL (delete): \u2421
blank space:  \u2422
open box:     \u2423
new line:     \u2424
delete form:  \u2425
substitute:   \u2426
'''


descriptions = {
  0x00 : 'null',
  0x01 : 'start of heading',
  0x02 : 'start of text',
  0x03 : 'end of text',
  0x04 : 'end of transmission',
  0x05 : 'enquiry',
  0x06 : 'acknowledge',
  0x07 : 'bell',
  0x08 : 'Backspace',
  0x09 : 'character tabulation',
  0x0A : 'line feed',
  0x0B : 'vertical tabulation',
  0x0C : 'form feed',
  0x0D : 'carriage return',
  0x0E : 'shift out',
  0x0F : 'shift in',
  0x10 : 'data link escape',
  0x11 : 'device control one (XON)',
  0x12 : 'device control two',
  0x13 : 'device control three (XOFF)',
  0x14 : 'device control four',
  0x15 : 'negative acknowledge',
  0x16 : 'synchronous idle',
  0x17 : 'end of transmission block',
  0x18 : 'cancel',
  0x19 : 'end of medium',
  0x1A : 'substitute',
  0x1B : 'escape',
  0x1C : 'file separator',
  0x1D : 'group separator ',
  0x1E : 'record separator',
  0x1F : 'unit separator',

  0x80 : 'Padding Character',
  0x81 : 'High Octet Preset',
  0x82 : 'Break Permitted Here',
  0x83 : 'No Break Here',
  0x84 : 'Index',
  0x85 : 'Next Line',
  0x86 : 'Start of Selected Area',
  0x87 : 'End of Selected Area',
  0x88 : 'Character Tabulation Set',
  0x89 : 'Character Tabulation With Justification',
  0x8A : 'Line Tabulation Set',
  0x8B : 'Partial Line Forward',
  0x8C : 'Partial Line Backward',
  0x8D : 'Reverse Line Feed',
  0x8E : 'Single-Shift 2',
  0x8F : 'Single-Shift 3',
  0x90 : 'Device Control String',
  0x91 : 'Private Use 1',
  0x92 : 'Private Use 2',
  0x93 : 'Set Transmit State',
  0x94 : 'Cancel character',
  0x95 : 'Message Waiting',
  0x96 : 'Start of Protected Area',
  0x97 : 'End of Protected Area',
  0x98 : 'Start of String',
  0x99 : 'Single Graphic Character Introducer',
  0x9A : 'Single Character Introducer',
  0x9B : 'Control Sequence Introducer',
  0x9C : 'String Terminator',
  0x9D : 'Operating System Command',
  0x9E : 'Privacy Message',
  0x9F : 'Application Program Command',
}


for i in range(0xff):
  if i < 0x20: # ascii control code; use control picture.
    c = i + 0x2400
  elif i == 0x20: # sp
    c = 0x2420
  elif i == 0x7f: # del; use control picture.
    c = 0x2421
  elif i >= 0x80 and i <= 0xa0:
    c = 0x2426 # no symbol available
  else:
    c = i

  d = descriptions.get(i, '')
  print('{:>4} {:03}: {}{}{}'.format(hex(i), i, chr(c), (' ' if d else ''), d))
