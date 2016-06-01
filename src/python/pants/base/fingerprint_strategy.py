# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

from abc import abstractmethod

from pants.base.fingerprint_log import FingerprintLog, logged_hasher
from pants.util.meta import AbstractClass


class DefaultFingerprintHashingMixin(object):
  """Default definitions for __hash__ and __eq__.

  Warning: Don't use this when the mixed in class has instance attributes mixed into its
  fingerprints.  This will cause subtle bugs because fingerprints are cached on the Target
  base class, and the cache key is the instance of the FingerprintStrategy."""

  def __hash__(self):
    return hash(type(self))

  def __eq__(self, other):
    return type(self) == type(other)


class FingerprintStrategy(AbstractClass):
  """A helper object for doing per-task, finer grained invalidation of Targets."""

  @abstractmethod
  def compute_fingerprint(self, target):
    """Subclasses override this method to actually compute the Task specific fingerprint."""

  def fingerprint_target(self, target):
    """Consumers of subclass instances call this to get a fingerprint labeled with the name"""
    fingerprint = self.compute_fingerprint(target)
    if fingerprint:
      return '{fingerprint}-{name}'.format(fingerprint=fingerprint, name=type(self).__name__)
    else:
      return None

  @abstractmethod
  def __hash__(self):
    """Subclasses must implement a hash so computed fingerprints can be safely memoized."""

  @abstractmethod
  def __eq__(self, other):
    """Subclasses must implement an equality check so computed fingerprints can be safely memoized."""


class DefaultFingerprintStrategy(DefaultFingerprintHashingMixin, FingerprintStrategy):
  """The default FingerprintStrategy, which delegates to target.payload.invalidation_hash().

  :API: public
  """

  def compute_fingerprint(self, target):
    """
    :API: public
    """
    return target.payload.fingerprint()


class TaskIdentityFingerprintStrategy(FingerprintStrategy):
  """Fingerprint strategy which includes the current task fingerprint when fingerprinting target.

  :API: public
  """

  def __init__(self, task):
    self._task = task

  def _build_hasher(self, target):
    with FingerprintLog.in_subscope(type(self._task).__name__):
      hasher = logged_hasher()
      with FingerprintLog.in_subscope(target.id):
        logged_hasher().update(target.payload.fingerprint() or '', name='target_fingerprint')
      hasher.update(self._task.fingerprint or '', name='task_fingerprint')
      return hasher

  def compute_fingerprint(self, target):
    """
    :API: public
    """
    hasher = self._build_hasher(target)
    return hasher.hexdigest()

  def __hash__(self):
    return hash(self._task.fingerprint)

  def __eq__(self, other):
    return self._task.fingerprint == other._task.fingerprint
