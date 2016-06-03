# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import logging
import os
from contextlib import contextmanager
from hashlib import sha1


logger = logging.getLogger(__name__)


class FingerprintLog(object):
  """Logs what information went into the creation of a fingerprint.

  The purpose of this class is to provide insight into why particular targets are getting
  invalidated. This may help users debug cache-thrashing problems.
  """

  class LoggedHasher(object):
    """A hasher wrapper that logs the hashing process."""

    def __init__(self, log, hasher):
      self._logger = log
      self._hasher = hasher
      self._index = 0

    def update(self, value, name=None):
      if name is None:
        name = str(self._index)
        self._index += 1
      self._hasher.update(value)
      self._logger.log(name, value)

    def log(self, key, *message):
      self._logger.log(str(key), ' '.join(map(str, message)))

    def hexdigest(self):
      return self._hasher.hexdigest()

  __current_scope = None
  __logs_by_scope = {}
  __logfile_path = None

  @classmethod
  def export_json(cls):
    sorted_instances = sorted(cls.__logs_by_scope.values(), key=lambda x: x.scope)
    return {instance.scope: instance._fields for instance in sorted_instances}

  @classmethod
  def for_scope(cls, scope):
    scope = scope or ''
    if scope not in cls.__logs_by_scope:
      cls.__logs_by_scope[scope] = cls(scope)
    return cls.__logs_by_scope[scope]

  @classmethod
  def global_instance(cls):
    return cls.for_scope('')

  @classmethod
  def current_instance(cls):
    return cls.for_scope(cls.__current_scope or '')

  @classmethod
  def in_subscope(cls, scope):
    return cls.in_scope(cls.current_instance().subscope(scope).scope)

  @classmethod
  @contextmanager
  def in_scope(cls, scope):
    try:
      current_scope = cls.__current_scope
      cls.__current_scope = scope
      yield cls.current_instance()
    finally:
      cls.__current_scope = current_scope

  def __init__(self, scope=''):
    self._fields = []
    self._scope = scope
    self._hasher = None

  @property
  def scope(self):
    return self._scope

  def subscope(self, scope):
    if not scope:
      raise ValueError('Subscope cannot be empty (got "{}").'.format(scope))
    return FingerprintLog.for_scope('/'.join([self._scope, scope]) if self._scope else scope)

  def log(self, key, value):
    self._fields.append((key, value))
    logger.info('[{}] {} = {}'.format(self.scope, key, value))
    # XXX THIS IS A HACK
    # This is a terrible, terrible hack and should *never* be used in a production version of pants!
    # I'm just commiting this to debug stuff.
    if FingerprintLog.__logfile_path is None:
      FingerprintLog.__logfile_path = os.path.abspath('dist/fingerprinting-report.txt')
    path = FingerprintLog.__logfile_path
    if not os.path.exists(os.path.dirname(path)):
      os.makedirs(os.path.dirname(path))
    with open(path, 'w') as f:
      f.write('\n'.join(sorted(
        '{}\t{}\t{}'.format(s, k, v)
        for s, x in FingerprintLog.__logs_by_scope.items() for k, v, in x._fields
      )))
      # f.write(json.dumps(
      #   FingerprintLog.export_json(),
      #   indent=4,
      #   separators=(',', ': '),
      #   sort_keys=True,
      # ))

  def hasher(self):
    if self._hasher is None:
      self._hasher = FingerprintLog.LoggedHasher(self, sha1())
    return self._hasher


def logged_hasher(subscope=None):
  instance = FingerprintLog.current_instance()
  if subscope:
    instance = instance.subscope(subscope)
  return instance.hasher()
