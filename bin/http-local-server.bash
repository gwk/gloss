#!/usr/bin/env bash
# Copyright 2011 George King. Permission to use this file is granted in license-gloss.txt.

echo "http://localhost:8000"
exec python3 -m http.server
