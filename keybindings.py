#!/usr/bin/env python3

import re
from sys import argv
from pithy.fs import append_path_stem_suffix, path_stem
from pithy.io import errL, errSL, outL, writeL
from pithy.iterable import group_by_heads
from pithy.json import JSONDecodeError, parse_json, write_json
from pithy.immutable import Immutable


def main():
  # paths passed in by make.
  defaults_json_path, bindings_path, out_path = argv[1:]

  defaults_out_path = "_build/vscode-keys-defaults.txt"
  whens_out_path= "_build/vscode-whens.txt"
  defaults, other_cmds = parse_defaults(defaults_json_path)

  def msg(line, *items):
    errSL(f'{bindings_path}:{line}:', *items)

  def warn(line, *items): msg(line, 'warning:', *items)

  def error(line, *items):
    msg(line, 'error:', *items)
    exit(1)

  ctx = Immutable(
    defaults=defaults,
    other_cmds=other_cmds,
    all_cmds=set(known_extension_cmds),
    all_whens=set(),
    dflt_triples=[], # used to generate keybindings.txt once.
    bindings=[],
    bound_cmds = set(),
    warn=warn,
    error=error)

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
  comment_re = re.compile(r'\s*//\s*(-)?\s*(.*)')
  # the defaults file contains comments, which the json parser rejects.
  for line in open(defaults_path):
    m = comment_re.match(line)
    if m: # commented line.
      if m[1]: # contains dash; assume one of the "other available commands."
        cmd = m[2].strip()
        assert cmd
        other_cmds.append(cmd)
    else:
      json_lines.append(line)

  # parse the filtered json.
  json_str = ''.join(json_lines)
  try: defaults = parse_json(json_str)
  except JSONDecodeError as e:
    line = e.lineno
    exit(f'{defaults_path}:{line}: error: {e}\n{json_lines[line-1]}')
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
    when_clause = f'when {when}' if when else ''
    writeL(f, f'{cmd:<63} {key:23} {when_clause}'.strip())


def write_whens(path, all_whens):
  f = open(path, 'w')
  for when in sorted(all_whens):
    writeL(f, when)


def parse_bindings(ctx, bindings_path):
  numbered_lines = enumerate(open(bindings_path), 1)
  for binding in group_by_heads(numbered_lines, is_head=lambda p: not p[1].startswith(' ')):
    parse_binding(ctx, binding)


def parse_binding(ctx, binding):
  line_num, line = binding[0] # first line.
  words = line.split()
  if not words: return
  cmd = words[0]
  if cmd not in ctx.all_cmds:
    ctx.warn(line_num, 'unknown command:', cmd)
  try:
    when_index = words.index('when')
  except ValueError:
    keys = words[1:]
    whens = []
  else:
    keys = words[1:when_index]
    whens = words[when_index+1:]
  ctx.bound_cmds.add(cmd)
  if not keys: return
  validate_keys(line_num, keys)
  validate_whens(ctx, line_num, whens)

  if len(binding) == 1:
    args = None
  else:
    args_str = ''.join(l for i, l in binding[1:])
    try: args = parse_json(args_str)
    except JSONDecodeError as e:
      ctx.error(line_num, f'invalid args JSON: {e}\n{args_str}')

  def add_binding(keys):
    binding = {
      'command': cmd,
      'key': ' '.join(keys)
    }
    if whens:
      binding['when'] = ' '.join(whens)
    if args is not None:
      binding['args'] = args
    ctx.bindings.append(binding)

  add_binding(keys)
  if keys == ['escape']: add_binding(['ctrl+c'])


def validate_keys(line_num, keys):
  for word in keys:
    for el in word.split('+'):
      if not key_validator.fullmatch(el):
        ctx.error(line_num, f'bad key: {el!r}')

def validate_whens(ctx, line_num, whens):
  for when in whens:
    if when.lstrip('!') not in ctx.all_whens:
      ctx.error(line_num, f'bad when: {when}')


def warn_unbound_cmds(ctx):
  unbound = ctx.all_cmds - ctx.bound_cmds
  if not unbound: return
  errL('\nunbound commands:')
  for cmd in sorted(unbound):
    errL(cmd)
  errL()

# https://code.visualstudio.com/docs/getstarted/keybindings#_accepted-keys
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

known_extension_cmds = {
  'settings.cycle.trimTrailingWhitespace',
}

main()
