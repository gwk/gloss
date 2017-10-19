#!/usr/bin/env python3
# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import re
from sys import stdin
from html.parser import HTMLParser
from argparse import ArgumentParser
from pithy.io import *


def main():
  parser = ArgumentParser('Check the validity of HTML documents.')
  parser.add_argument('paths', nargs='*', help='paths to HTML documents (defaults to stdin).')
  args = parser.parse_args()

  try: files = [open(path) for path in args.paths]
  except FileNotFoundError as e: exit(f'file not found: {e.filename}')
  if not files: files = [stdin]

  for file in files:
    parser = Parser(path=file.name, convert_charrefs=True)
    parser.feed(file.read())
    parser.close()


class Parser(HTMLParser):

  def __init__(self, path: str, convert_charrefs: bool) -> None:
    super().__init__(convert_charrefs=convert_charrefs)
    self.path = path
    self.stack = []

  def msg(self, msg, pos=None):
    if pos is None: pos = self.getpos()
    outL(f'{self.path}:{pos[0]}:{pos[1]}: {msg}')

  def handle_startendtag(self, tag, attrs):
    pass

  def handle_starttag(self, tag, attrs):
    self.stack.append((self.getpos(), tag))

  def handle_endtag(self, tag):
    if not self.stack:
      self.msg(f'unmatched closing tag at top level: {tag}')
      return
    if self.stack[-1][1] == tag:
      self.stack.pop()
      return
    for i in reversed(range(len(self.stack))):
      if self.stack[i][1] == tag: # found match.
        self.msg(f'unmatched closing tag is ambiguous: {tag}')
        self.msg(f'note: could match here', pos=self.stack[i][0])
        for p, _ in self.stack[i+1:]:
          self.msg(f'note: ignoring opening tag here', pos=p)
        return
    self.msg(f'unmatched closing tag: {tag}')

  def handle_decl(self, decl):
    self.msg(f'decl: {decl!r}')

  def unknown_decl(data):
    self.msg(f'unknown decl: {data!r}')

  def handle_data(self, data): pass

  def handle_pi(self, data):
    self.msg(f'processing instruction: {data!r}')


if __name__ == '__main__': main()
