# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).



from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                                                                                     print_function, unicode_literals)

import logging
import os
import re
import shutil

from pants.backend.core.tasks.task import Task
from pants.backend.jvm.targets.jar_source_set import JarSourceSet
from pants.base.address_lookup_error import AddressLookupError
from pants.base.build_environment import get_buildroot
from pants.base.source_root import SourceRoot
from pants.fs.archive import ZIP

from twitter.common.dirutil.fileset import fnmatch_translate_extended
from twitter.common.collections import OrderedSet, maybe_list


logger = logging.getLogger(__name__)


class UnpackJarSourceSet(Task):

  class WrongTargetTypeError(Exception):
    """Thrown if a reference to a non jar_source_set is listed in the arguments."""
    pass

  class ExpectedAddressError(Exception):
    """Thrown if an object that is not an address is listed in the arguments."""
    pass

  def __init__(self, *args, **kwargs):
    super(UnpackJarSourceSet, self).__init__(*args, **kwargs)
    self._buildroot = get_buildroot()

  def prepare(self, round_manager):
    super(UnpackJarSourceSet, self).prepare(round_manager)
    round_manager.require_data('ivy_imports')

  def resolve_deps(self, key, default=[]):
    deps = OrderedSet()
    for dep in self.context.config.getlist('unpack-jar-source-set', key, default=maybe_list(default)):
      if dep:
        try:
          deps.update(self.context.resolve(dep))
        except AddressLookupError as e:
          raise self.DepLookupError("{message}\n  referenced from [{section}] key: {key} in pants.ini"
                                    .format(message=e, section='protobuf-gen', key=key))
    return deps

  def _jar_source_set_unpack_dir(self, jar_source_set):
    return os.path.normpath(os.path.join(self._workdir, jar_source_set.id))

  def _unpack(self, jar_source_set):
    """Extracts files from the downloaded jar files and places them in a work directory.

    :param JarSourceSet jar_source_set: target referencing jar_libraries to unpack.
    """
    unpack_dir = self._jar_source_set_unpack_dir(jar_source_set)
    if os.path.exists(unpack_dir):
      shutil.rmtree(unpack_dir)
    if not os.path.exists(unpack_dir):
      os.makedirs(unpack_dir)

    include_patterns = [re.compile(fnmatch_translate_extended(i))
                        for i in jar_source_set.include_patterns]
    exclude_patterns = [re.compile(fnmatch_translate_extended(e))
                        for e in jar_source_set.exclude_patterns]

    def _unpack_filter(filename):
      if include_patterns:
        found = False
        for include_pattern in include_patterns:
          if include_pattern.match(filename):
            found = True
            break;
        if not found:
          return False
      if exclude_patterns:
        for exclude_pattern in exclude_patterns:
          if exclude_pattern.match(filename):
            return False
      return True

    products = self.context.products.get('ivy_imports')
    jarmap = products[jar_source_set]

    for path, names in jarmap.items():
      for name in names:
        jar_path = os.path.join(path, name)
        ZIP.extract(jar_path, unpack_dir, filter=_unpack_filter)

  def execute(self):
    def add_jar_source_sets(target):
      if isinstance(target, JarSourceSet):
        jar_source_sets.add(target)

    jar_source_sets = set()
    targets = self.context.targets()
    addresses = [target.address for target in targets]
    self.context.build_graph.walk_transitive_dependency_graph(addresses, add_jar_source_sets)
    for jar_source_set in jar_source_sets:
      self._unpack(jar_source_set)
      unpack_dir = self._jar_source_set_unpack_dir(jar_source_set)
      found_files = []
      for root, dirs, files in os.walk(unpack_dir):
        for f in files:
          relpath = os.path.relpath(os.path.join(root, f), unpack_dir)
          found_files.append(relpath)
      rel_unpack_dir = unpack_dir[len(self._buildroot) + 1:]
      SourceRoot.register(rel_unpack_dir)
      jar_source_set.populate(found_files, rel_path=rel_unpack_dir, source_root=unpack_dir)
