#!/usr/bin/env bash
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

echo "http://localhost:8000"
exec python3 -m http.server
