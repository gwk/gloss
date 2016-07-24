#!/usr/bin/env python3

import re
from pithy import (
  append_path_stem_suffix,
  argv,
  checkF,
  errFL, errL, errSL,
  Immutable,
  outFL,
  parse_json, path_stem,
  writeL, write_json
)


def main():
  # paths passed in by make.
  defaults_json_path, bindings_path, out_path = argv[1:]

  defaults_out_path = "_build/vscode-keys-defaults.txt"
  whens_out_path= "_build/vscode-whens.txt"
  defaults, other_cmds = parse_defaults(defaults_json_path)

  ctx = Immutable(
    defaults=defaults,
    other_cmds=other_cmds,
    all_cmds=set(),
    all_whens=set(),
    dflt_triples=[], # used to generate keybindings.txt once.
    bindings=[],
    bound_cmds = set())

  prepare(ctx)
  write_defaults_txt(defaults_out_path, ctx.dflt_triples)
  write_whens(whens_out_path, ctx.all_whens)
  parse_bindings(ctx, bindings_path)
  warn_unbound_cmds(ctx)

  out_file = open(out_path, 'w')
  write_json(out_file, ctx.bindings)



def parse_defaults(defaults_path):
  json_lines = []
  other_cmds = []

  # the defaults file contains comments, which the json parser rejects.
  for line in open(defaults_path):
    if line.startswith('//'):
      _, _, cmd = line.partition('// - ') # distinguishes the 'other available commands'.
      if cmd:
        other_cmds.append(cmd.strip())
    else:
      json_lines.append(line)

  # parse the filtered json.
  json_str = ''.join(json_lines)
  defaults = parse_json(json_str)
  return defaults, other_cmds


def prepare(ctx):
  # nullify each default by adding a matching rule with a negating command.
  # additionally, accumulate all cmds and whens.
  for dflt in ctx.defaults:
    key = dflt['key']
    cmd = dflt['command']
    ctx.all_cmds.add(cmd)
    nullification = {
      'key': key,
      'command': '-' + cmd
    }
    when = dflt.get('when', '')
    if when:
      for word in when.split():
        ctx.all_whens.add(word.lstrip('!'))
      nullification['when'] = when
    ctx.bindings.append(nullification)
    ctx.dflt_triples.append((cmd, key, when))
  for cmd in ctx.other_cmds:
    ctx.all_cmds.add(cmd)
    ctx.dflt_triples.append((cmd, '', ''))


def write_defaults_txt(path, dflt_triples):
  'generate keybindings.txt as starting point for customization.'
  f = open(path, 'w')
  for (cmd, key, when) in sorted(dflt_triples):
    when_clause = 'when ' + when if when else ''
    writeL(f, '{:<63} {:23} {}'.format(cmd, key, when_clause).strip())


def write_whens(path, all_whens):
  f = open(path, 'w')
  for when in sorted(all_whens):
    writeL(f, when)


def parse_bindings(ctx, bindings_path):
  for line_num, line in enumerate(open(bindings_path), 1):
    parse_binding(ctx, line_num, line)


def parse_binding(ctx, line_num, line):
  words = line.split()
  if not words: return
  cmd = words[0]
  if cmd not in ctx.all_cmds:
    errFL('warning: {}: unknown command: {}', line_num, cmd)
  try:
    when_index = words.index('when')
  except ValueError:
    keys = words[1:]
    whens = []
  else:
    keys = words[1:when_index]
    whens= words[when_index+1:] 
  ctx.bound_cmds.add(cmd)
  if not keys: return
  validate_keys(line_num, keys)
  binding = {
    'command': cmd,
    'key': ' '.join(keys)
  }
  if whens:
    validate_whens(ctx, line_num, whens)
    binding['when'] = ' '.join(whens)
  ctx.bindings.append(binding)



key_validator = re.compile(r'''(?x)
  alt
| cmd
| ctrl
| escape
| shift
| space | backspace | delete | enter | tab
| up | down | left | right
| pageup| pagedown | home | end
| f(?:\d{1,2})
| \\?[][-zA-Z0-9\'"`.,;/\\=-]
''')

def validate_keys(line_num, keys):
  for word in keys:
    for el in word.split('+'):
      checkF(key_validator.fullmatch(el), '{}: bad key: {!r}', line_num, el)

def validate_whens(ctx, line_num, whens):
  for when in whens:
    checkF(when.lstrip('!') in ctx.all_whens, '{}: bad when: {}', line_num, when)


def warn_unbound_cmds(ctx):
  unbound = ctx.all_cmds - ctx.bound_cmds
  if not unbound: return
  errL('\nunbound commands:')
  for cmd in sorted(unbound):
    errL('  ', cmd)

main()
