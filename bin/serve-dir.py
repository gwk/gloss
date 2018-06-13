#!/usr/bin/env python3
# # Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

from argparse import ArgumentParser
from functools import partial
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, HTTPServer
from os import fstat as os_fstat
from posixpath import normpath
import time
from typing import *
from typing import BinaryIO
from urllib.parse import unquote as url_unquote, urlsplit as url_split, urlunsplit as url_join
from pithy.task import run
from pithy.fs import *
from pithy.io import *


def main():
  parser = ArgumentParser(description='Serve files from a directory.')
  parser.add_argument('root', default='.', nargs='?', help='Root directory to serve from')
  parser.add_argument('-browser', help='Launch the specified browser')
  parser.add_argument('-safari',  action='store_true', help='Launch Safari')
  parser.add_argument('-chrome',  action='store_true', help='Launch Google Chrome')
  parser.add_argument('-firefox', action='store_true', help='Launch Firefox')

  args = parser.parse_args()
  root = args.root
  address = ('localhost', 8000) # TODO: argparse option.
  host, port = address
  addr_str = f'http://{host}:{port}'
  errL(addr_str)

  ignored_paths = {
    'apple-touch-icon-precomposed.png',
  }


  class Handler(SimpleHTTPRequestHandler):

    def __init__(self, *args, **kwargs) -> None:
      '''
      Unfortunately SimpleHTTPRequestHandler handles the request directly from __init__.
      This means that the only thing we can really do here is default initializations.
      '''
      self.local_path: Optional[str] = None
      try:
        super().__init__(directory=root, *args, **kwargs)
      except:
        errSL(f'url path: {self.path}; local_path: {self.local_path}')
        raise

    def parse_request(self) -> bool:
      '''
      Compute local_path as a derivative of path, which is computed by call to super.
      '''
      if not super().parse_request(): return False
      # Compute local_path.
      p = self.path
      # abandon query parameters.
      p = p.partition('?')[0]
      p = p.partition('#')[0]
      has_trailing_slash = p.rstrip().endswith('/') # remember explicit trailing slash.
      p = url_unquote(p)
      p = normpath(p)
      if '..' in p: return
      assert p.startswith('/')
      p = p[1:] # Remove leading slash. TODO: path_join should not use os.path.join, which behaves dangerously for absolute paths.
      p = norm_path(path_join(self.directory, p))
      if has_trailing_slash: p += '/'
      self.local_path = p
      return True

    def log_message(self, format, *args) -> None:
      'Base logging function called by all others. Overridden to alter formatting.'
      errL(f'{self.log_date_time_string()}: {self.address_string()} - {format%args}')

    def log_request(self, code='-', size='-') -> None:
      '''
      Log an accepted request; called by send_response().
      Overridden to print code.phrase and local_path.
      '''
      assert isinstance(code, HTTPStatus)
      self.log_message('%s %s "%s": %s', code.value, code.phrase, self.requestline, self.local_path)

    def log_date_time_string(self) -> str:
      'Overridden to use lexicographic format.'
      now = time.time()
      year, month, day, hh, mm, ss, wd, yd, is_dst = time.localtime(now)
      return f'{year:04}-{month:02}-{day:02} {hh:02}:{mm:02}:{ss:02}.{now%1:.03f}'


    def send_response(self, code:HTTPStatus, message=None) -> None:
      'Send response headers to prevent all caching.'
      super().send_response(code=code, message=message)
      self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
      self.send_header('Pragma', 'no-cache')
      self.send_header('Expires', '0')


    def send_head(self) -> Optional[BinaryIO]:
      if self.path == '/favicon.ico': # TODO: send actual favicon if it exists.
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'image/x-icon')
        self.send_header('Content-Length', 0)
        self.end_headers()
        return None

      if self.local_path is None:
        self.send_error(HTTPStatus.UNAUTHORIZED, "Path refers to parent directory")
        return None

      if is_dir(self.local_path):
        if not self.local_path.endswith('/'): # redirect browser to path with slash (what apache does).
          self.send_response(HTTPStatus.MOVED_PERMANENTLY)
          parts = list(url_split(self.path))
          parts[2] += '/'
          new_url = url_join(parts)
          self.send_header("Location", new_url)
          self.end_headers()
          return None
        for index in ("index.html", "index.htm"):
          index = path_join(self.local_path, index)
          if path_exists(index):
            self.local_path = index
            break
        else:
          return self.list_directory(self.local_path)

      ctype = self.guess_type(self.local_path)
      f: BinaryIO
      try:
        f = open(self.local_path, 'rb')
      except OSError:
        self.send_error(HTTPStatus.NOT_FOUND,
          message=f'File not found: {self.local_path}',
          explain=f'URI path: {self.path}')
        return None
      try:
        f_stat = os_fstat(f.fileno())
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-type", ctype)
        self.send_header("Content-Length", str(f_stat[6]))
        self.send_header("Last-Modified", self.date_time_string(f_stat.st_mtime))
        self.end_headers()
        return f
      except:
        f.close()
        raise


    def translate_path(self, path: str) -> str:
      raise Exception('should never be called; use self.local_path instead.')


  server = HTTPServer(address, Handler)

  # note: the way we tell the OS to open the URL in the browser is a rather suspicious hack:
  # the `open` command returns and then we launch the web server,
  # relying on the fact that together the OS and the launched browser take more time to initiate the request
  # after the `open` process completes than the server does to initialize.
  if args.browser:  run(['open', '-a', args.browser,    addr_str])
  if args.safari:   run(['open', '-a', 'safari',        addr_str])
  if args.chrome:   run(['open', '-a', 'google chrome', addr_str])
  if args.firefox:  run(['open', '-a', 'firefox',       addr_str])

  try: server.serve_forever()
  except KeyboardInterrupt:
    errL('\nKeyboard interrupt received; shutting down.')
    exit()


if __name__ == '__main__': main()
