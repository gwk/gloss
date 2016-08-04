#!/usr/bin/env python3
# Copyright 2009 George King. Permission to use this file is granted in license-gloss.txt.

# total hours in a timesheet.

# format is:

# 12:00 begin
# 18:30 change tasks
# 24:00 end = 12:00

import optparse
import os
import re

from pithy.io import checkS, outF, outL, outFL


def minutes(match):
  return int(match.group(1)) * 60 + int(match.group(2))


optparser = optparse.OptionParser(usage='usage: %prog root_path [hourly_rate]')
(options, args) = optparser.parse_args()

if len(args) < 1:
  optparser.error('no arguments')

path = args[0]

hourly_rate = float(args[1]) if len(args) > 1 else 0

if len(args) > 2:
  print(args)
  optparser.error('too many arguments')

time_re     = re.compile(r'(\d{2}):(\d{2}) ')
subtotal_re = re.compile(r'= (\d{1,2}):(\d{2})')
money_re    = re.compile(r'([+-])\s*\$(\d+)(\.?\d*)')

checkS(os.path.isfile(path), Exception, 'bad path:', path)

start_minutes = None
end_minutes   = None
total_minutes = 0
total_payment = 0
total_expense = 0

valid = True

with open(path) as f:
  for line in f: 
    outF('{:64}', line.rstrip('\n'))
    time_match = time_re.match(line)
    
    if time_match:
      m = minutes(time_match)
      if start_minutes == None:   start_minutes = m
      else:                       end_minutes = m
      outF('|{:4} ', m)

    subtotal_match = subtotal_re.search(line)
    
    if subtotal_match:
      assert start_minutes != None
      assert end_minutes != None
      sub_minutes = end_minutes - start_minutes
      total_minutes += sub_minutes
      start_minutes = None
      end_minutes = None
      m = minutes(subtotal_match)
      outF('= {:4}m', sub_minutes)
      if m != sub_minutes:
        outF(' *** found: {}; calculated: {}',  m, sub_minutes)
        valid = False

    money_match = money_re.match(line)
    if money_match:
      s = ''.join(money_match.groups())
      i = float(s)
      if (i < 0):
        total_payment += i
      else:
        total_expense += i
      outF('               {: 10,.2f}', i)
    
    outL()


hours = total_minutes // 60
rem_minutes = int(total_minutes) % 60
time_expense = hourly_rate * total_minutes / 60

if hourly_rate:
  hourly_string = ' @ {:0.2f}/hr = ${:,.2f}'.format(hourly_rate, time_expense)
else:
  hourly_string = ''

outL()
outFL('TOTAL HOURS:   {:2}:{:02}{}', hours, rem_minutes, hourly_string)
outFL('TOTAL EXPENSE: ${:,.2f}', total_expense)
outFL('TOTAL PAYMENT: ${:,.2f}', total_payment)
outFL('TOTAL:         ${:,.2f}', time_expense + total_payment + total_expense)

if not valid:
  outL('*** INVALID ***')
