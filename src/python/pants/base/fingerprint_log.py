# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import logging
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
      self._log = log
      self._hasher = hasher
      self._index = 0

    def update(self, value, name=None):
      if name is None:
        name = str(self._index)
        self._index += 1
      self._hasher.update(value)
      self._log(name, value)

    def hexdigest(self):
      return self._hasher.hexdigest()

  __current_scope = None
  __logs_by_scope = {}

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
    return cls.in_scope(cls.current_instance().subscope(scope))

  @classmethod
  @contextmanager
  def in_scope(cls, scope):
    try:
      current_scope = cls.__current_scope
      cls.__current_scope = scope
      yield
    finally:
      cls.__current_scope = current_scope

  def __init__(self, scope=''):
    self._fields = {}
    self._scope = scope

  @property
  def scope(self):
    return self._scope

  def subscope(self, scope):
    if not scope:
      raise ValueError('Subscope cannot be empty (got "{}").'.format(scope))
    return FingerprintLog.for_scope('.'.join(self._scope, scope) if self._scope else scope)

  def log(self, key, value):
    self._fields[key] = value
    logger.info('[{}] {} = {}'.format(self.scope, key, value))

  def hasher(self, hasher=None):
    return FingerprintLog.LoggedHasher(self, hasher or sha1())


def logged_hasher():
  return FingerprintLog.current_instance().hasher()
