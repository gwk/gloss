#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import plistlib
from sys import stdout

from pithy.fs import walk_files
from pithy.io import outL
from pithy.json import load_json
from pithy.schema import Schema, compile_schema, write_schema


themes_dir = '/Applications/Visual Studio Code.app/Contents/Resources/app/extensions/theme-defaults/themes'

themes = []

for path in walk_files(themes_dir, file_exts=['.json', '.tmlanguage']):
  outL(path)
  if path.endswith('.json'):
    theme = load_json(open(path))
  else:
    theme = plistlib.load(open(path, 'rb'))
  themes.append(theme)

schema = Schema()
schema = compile_schema(nodes=themes, schema=schema)

outL()
write_schema(stdout, schema)
