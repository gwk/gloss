#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

'''
Serve stdin to a new browser window.
'''

import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from sys import argv, stdin


args = argv[1:]
if len(args) > 1:
  exit('specify a single argument or pipe to stdin.')

path = args[0] if args else None

if path:
  f = open(path, 'rb')
else:
  f = stdin.detach()


class Handler(BaseHTTPRequestHandler):

  def do_HEAD(self):
    self.send_response(200)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()

  def do_GET(self):
    self.send_response(200)
    self.send_header('Content-Type', 'text/html')
    self.end_headers()
    for line in f:
      self.wfile.write(line)
      self.wfile.flush()


host, port = address = ('localhost', 8000)
addr_str = 'http://{}:{}'.format(host, port)
#print(addr_str)
server = HTTPServer(address, Handler)
subprocess.Popen(['open', addr_str]) # race condition!
server.handle_request()
