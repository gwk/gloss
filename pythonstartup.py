# Dedicated to the public domain under CC0: https://creativecommons.org/publicdomain/zero/1.0/.

import collections
import collections.abc
import dataclasses
import enum
import functools
import importlib
import inspect
import io
import itertools
import math
import operator
import os
import re
import sys
import textwrap
import time
import typing
import zoneinfo

# Import typing first so that other imports take precedence, particularly the collections and collections.abc types.
from typing import (Literal, TypeGuard, overload, TypeVar, Any, Callable, Iterator, Iterable, Sequence, Mapping, MutableMapping,
  Union, Optional, overload, Protocol, runtime_checkable)
from collections import *
from collections.abc import *

# Import copy symbols after dataclasses so that copy.replace is used.
from dataclasses import dataclass, field, fields
from copy import copy, deepcopy, replace

from enum import *
from functools import *
from importlib import *
from inspect import *
from io import *
from itertools import *
from math import *
from operator import *
from os import environ, uname
from sys import argv, stderr, stdout
from textwrap import indent, dedent
from time import monotonic, perf_counter, process_time, sleep
from zoneinfo import *


# Pithy imports are conditional.
try:
  import pithy
except ImportError:
  print('note: pithy package not found; skipping imports.', file=stderr)
else:
  import pithy.ansi
  import pithy.clock
  import pithy.collection
  import pithy.csv
  import pithy.date
  import pithy.default
  import pithy.desc
  import pithy.dict
  import pithy.fs
  import pithy.io
  import pithy.iterable
  import pithy.json
  import pithy.loader
  import pithy.path
  import pithy.range
  import pithy.reprs
  import pithy.sequence
  import pithy.strings
  import pithy.task
  import pithy.type_utils
  import pithy.typing_utils
  import pithy.untyped
  import pithy.url
  import pithy.util
  from pithy.ansi import *
  from pithy.clock import *
  from pithy.collection import *
  from pithy.csv import *
  from pithy.date import *
  from pithy.default import *
  from pithy.desc import *
  from pithy.dict import *
  from pithy.fs import *
  from pithy.io import *
  from pithy.iterable import *
  from pithy.json import *
  from pithy.loader import *
  from pithy.path import *
  from pithy.range import *
  from pithy.reprs import *
  from pithy.sequence import *
  from pithy.strings import *
  from pithy.task import *
  from pithy.type_utils import *
  from pithy.typing_utils import *
  from pithy.untyped import *
  from pithy.url import *
  from pithy.util import *
