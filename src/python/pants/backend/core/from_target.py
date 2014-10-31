# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import six

from pants.backend.core.targets.source_set import SourceSetAddresses


class FromTarget(object):
  """Used in a BUILD file to redirect the value of the sources= attribute to a SourceSet target.
  """
  class ExpectedAddressError(Exception):
    """Thrown if an object that is not an address is added to an import attribute.
    """

  def __init__(self, parse_context):
    """
    :param ParseContext parse_context: build file context
    """

  def __call__(self, address):
    """Expects a string representing an address."""
    if not isinstance(address, six.string_types):
      raise self.ExpectedAddressError("Expected string address argument, got type {type}"
                                     .format(type(address)))
    return SourceSetAddresses(addresses=[address])
