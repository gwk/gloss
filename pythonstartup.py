
# Import typing first so that other symbols take precedence.
# This is especially desirable for the collections symbols; the typing versions are deprecated.
import typing; from typing import *

import collections; from collections import *
import collections.abc; from collections.abc import *
import dataclasses; from dataclasses import *
import enum; from enum import *
import functools; from functools import *
import importlib; from importlib import *
import inspect; from inspect import *
import io; from io import *
import itertools; from itertools import *
import math; from math import *
import operator; from operator import *
import os; from os import environ
import re;
import sys; from sys import argv, stderr, stdout
import time; from time import *

import pithy.ansi; from pithy.ansi import *
import pithy.buffer; from pithy.buffer import *
import pithy.collection; from pithy.collection import *
import pithy.clock; from pithy.clock import *
import pithy.csv; from pithy.csv import *
import pithy.date; from pithy.date import *
import pithy.default; from pithy.default import *
import pithy.desc; from pithy.desc import *
import pithy.dict; from pithy.dict import *
import pithy.html; from pithy.html import *
import pithy.format; from pithy.format import *
import pithy.fs; from pithy.fs import *
import pithy.graph; from pithy.graph import *
import pithy.io; from pithy.io import *
import pithy.iterable; from pithy.iterable import *
import pithy.json; from pithy.json import *
import pithy.loader; from pithy.loader import *
import pithy.path; from pithy.path import *
import pithy.path_encode; from pithy.path_encode import *
import pithy.range; from pithy.range import *
import pithy.schema; from pithy.schema import *
import pithy.sequence; from pithy.sequence import *
import pithy.string; from pithy.string import *
import pithy.svg; from pithy.svg import *
import pithy.task; from pithy.task import *
import pithy.types; from pithy.types import *
import pithy.untyped; from pithy.untyped import *
import pithy.url; from pithy.url import *
import pithy.util; from pithy.util import *
import pithy.xml; from pithy.xml import *

# Currently buggy for 3.7.
#import jedi.utils
#jedi.utils.setup_readline()
