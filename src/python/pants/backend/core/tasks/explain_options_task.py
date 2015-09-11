# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from colors import black, blue, cyan, green, magenta, red, white

from pants.backend.core.tasks.console_task import ConsoleTask
from pants.option.option_tracker import OptionTracker
from pants.option.ranked_value import RankedValue


class ExplainOptionsTask(ConsoleTask):

  @classmethod
  def register_options(cls, register):
    super(ExplainOptionsTask, cls).register_options(register)
    register('--scope', help='Only show options in this scope.')
    register('--option', help='Only show options with this name.')
    register('--rank', choices=RankedValue.get_names(),
             help='Only show options with at least this importance.')
    register('--show-overridden', action='store_true', default=False,
             help='Show values that were overriden.')
    register('--only-overridden', action='store_true', default=False,
             help='Only show values that overrode defaults.')

  def _scope_filter(self, scope):
    pattern = self.get_options().scope
    if pattern and not scope.startswith(pattern):
      return False
    return True

  def _option_filter(self, option):
    pattern = self.get_options().option
    if not pattern:
      return True
    pattern = pattern.replace('-', '_')
    return option == pattern

  def _rank_filter(self, rank):
    pattern = self.get_options().rank
    if not pattern:
      return True
    return rank >= RankedValue.get_rank_value(pattern)

  def _rank_color(self, rank):
    if not self.get_options().colors:
      return lambda x: x
    if rank == RankedValue.NONE: return white
    if rank == RankedValue.HARDCODED: return white
    if rank == RankedValue.ENVIRONMENT: return red
    if rank == RankedValue.CONFIG: return blue
    if rank == RankedValue.FLAG: return magenta
    return black

  def _format_scope(self, scope, option):
    scope_color = cyan if self.get_options().colors else lambda x: x
    option_color = blue if self.get_options().colors else lambda x: x
    return '{scope}{option}'.format(
      scope=scope_color('{}.'.format(scope) if scope else ''),
      option=option_color(option),
    )

  def _format_record(self, record):
    value_color = green if self.get_options().colors else lambda x: x
    rank_color = self._rank_color(record.rank)
    return '{value} {rank}'.format(
      value=value_color(str(record.value)),
      rank=rank_color('(from {rank}{details})'.format(
        rank=RankedValue.get_rank_name(record.rank),
        details=' {}'.format(record.details) if record.details else '',
      )),
    )

  def _show_history(self, history):
    for record in reversed(list(history)[:-1]):
      if record.rank == RankedValue.NONE:
        continue # I don't think we care about None.
      yield '  overrode {}'.format(self._format_record(record))

  def _force_option_parsing(self):
    scopes = list(OptionTracker.option_history_by_scope.keys())
    for scope in scopes:
      self.context.options.for_scope(scope)

  def console_output(self, targets):
    self._force_option_parsing()
    for scope, options in sorted(OptionTracker.option_history_by_scope.items()):
      if not self._scope_filter(scope): continue
      for option, history in sorted(options.items()):
        if not self._option_filter(option): continue
        if not self._rank_filter(history.latest.rank): continue
        if self.get_options().only_overridden and len(history) <= 1:
          continue
        yield '{} = {}'.format(self._format_scope(scope, option),
                               self._format_record(history.latest))
        if self.get_options().show_overridden:
          for line in self._show_history(history):
            yield line
