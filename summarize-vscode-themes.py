#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import plistlib

from pithy import *
from pithy.schema import *


themes_dir = '/Applications/Visual Studio Code.app/Contents/Resources/app/extensions/theme-defaults/themes'

themes = []

for path in walk_files(themes_dir, file_exts=['.json', '.tmlanguage']):
  outL(path)
  if path.endswith('.json'):
    theme = read_json(open(path))
  else:
    theme = plistlib.load(open(path, 'rb'))
  themes.append(theme)

schema = compile_schema(*themes)

outL()
out_schema(schema)

outL('\nschema summary:\n')
out_schema(schema, summary=True)
