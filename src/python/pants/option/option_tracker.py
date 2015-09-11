# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from collections import defaultdict, namedtuple


class OptionTracker(object):

  OptionHistoryRecord = namedtuple('OptionHistoryRecord', ['value', 'rank', 'details'])

  class OptionHistory(object):
    def __init__(self):
      self.values = []

    def record_value(self, value, rank, details=None):
      if self.values:
        if self.latest.rank > rank:
          return
        if self.latest.value == value:
          return # No change.
      self.values.append(OptionTracker.OptionHistoryRecord(value, rank, details))

    @property
    def latest(self):
      return self.values[-1]

    def __iter__(self):
      for record in self.values:
        yield record

    def __len__(self):
      return len(self.values)

  option_history_by_scope = defaultdict(dict)

  @classmethod
  def record_option(cls, scope, option, value, rank, details=None):
    scoped_options = cls.option_history_by_scope[scope]
    if option not in scoped_options:
      scoped_options[option] = cls.OptionHistory()
    scoped_options[option].record_value(value, rank, details)
