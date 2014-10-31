# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).


from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from abc import abstractmethod
from collections import namedtuple
import logging
import os

from pants.base.address import SyntheticAddress, Address, parse_spec
from pants.base.target import Target
from pants.base.validation import assert_list

from twitter.common.dirutil.fileset import Fileset


logger = logging.getLogger(__name__)


# SourceSetAddresses: Used as a sentinel type for identifying a SourceSet declared in a build file.
# They might be relative specs, so they need to be interpreted relative to another address.
SourceSetAddresses = namedtuple('SourceSetAddresses', ['addresses'])

# TODO(Eric Ayers): If we want to keep the name SourceSet here, consider renaming SourceSet used in ide_gen.py
class SourceSet(Target):
  """Represents source files passed in to a target."""

  class UnexpectedSourceTypeError(Exception):
    """The wrong type of argument was passed to sources."""
    pass

  def __init__(self, rel_path=None, *args, **kwargs):
    """
      :param rel_path: common root for files
    """
    super(SourceSet, self).__init__(*args, **kwargs)
    self._rel_path = rel_path

  def is_empty(self):
    return len(self.files()) == 0

  @property
  def rel_path(self):
    return self._rel_path

  @abstractmethod
  def files(self):
    """
    :return: files represented by this object (relative to rel_path)
    :rtype: list of strings
    """

  def files_relative_to_buildroot(self):
    """
    :return: files with the rel_path prepended
    :rtype: list of strings
    """
    return [os.path.join(self.rel_path, f) for f in self.files()]

  @staticmethod
  def from_source_object(ref_address, sources_object, build_graph, rel_path=None):
    """Factory method for turning a fileset or list of strings into a SourceSet.

    :param Address ref_address: spec of target that references this source object (target may
    not be fully initialized)
    :param object sources_object: A fileset, list of strings, or another SourceSet object
    :param BuildGraph build_graph: The BuildGraph that this Target lives within
    :param string rel_path: directory that is the common root for files.
    :return: a SourceSet representing the fileset or list, or the original sources_object
    if it is already a SourceSet instance.
    """
    if isinstance(sources_object, SourceSet):
      return sources_object

    name = "internal-sources.{ref_name}".format(
      ref_name=ref_address.target_name)
    synthetic_address = SyntheticAddress(ref_address.spec_path, ref_address.path_safe_spec)

    if isinstance(sources_object, Fileset):
      return FilesetSourceSet(fileset=sources_object,
                              name=name,
                              address=synthetic_address,
                              build_graph=build_graph,
                              rel_path=rel_path)
    elif isinstance(sources_object, SourceSetAddresses):
      # TODO(Eric Ayers) SourceSetAddresses can take a list of addresses, but for now this
      # code is just setup to handle the first one.
      build_graph.inject_spec_closure(sources_object.addresses[0],
                                      relative_to=ref_address.spec_path)
      source_set_target = build_graph.get_target_from_spec(sources_object.addresses[0],
                                                           relative_to=ref_address.spec_path)
      if not isinstance(source_set_target, SourceSet):
        raise SourceSet.UnexpectedSourceTypeError("Expected a string, got type {name}"
                                                  .format(name=type(source_set_target).__name__))
      return source_set_target
    elif sources_object is None or isinstance(sources_object, (list, tuple)):
      return DefaultSourceSet(file_list=sources_object,
                              name=name,
                              address=synthetic_address,
                              build_graph=build_graph,
                              rel_path=rel_path)

    raise SourceSet.UnexpectedSourceTypeError(
      "Expected list of strings or instance of Sources "
      "for sources attribute. got {sources_type}"
      .format(sources_type=type(sources_object).__name__))


class FilesetSourceSet(SourceSet):
  """A SourceSet backed by a Fileset."""

  def __init__(self, fileset, *args, **kwargs):
    """:param Fileset fileset: a fileset containing sources"""
    super(FilesetSourceSet, self).__init__(*args, **kwargs)
    self._fileset = fileset

  def files(self):
    return [f for f in self._fileset]


class DefaultSourceSet(SourceSet):
  """A SourceSet backed by a list of strings representing filenames."""

  def __init__(self, file_list, *args, **kwargs):
    """
    :param list file_list: strings representing paths to files to use as sources
    """
    super(DefaultSourceSet, self).__init__(*args, **kwargs)
    self._files = assert_list(file_list)

  def files(self):
    return [f for f in self._files]