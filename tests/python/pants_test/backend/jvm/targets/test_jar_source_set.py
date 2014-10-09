# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from textwrap import dedent

from pants.base.address import SyntheticAddress

from pants.backend.jvm.targets.jar_dependency import JarDependency
from pants.backend.jvm.targets.jar_library import JarLibrary
from pants.backend.jvm.targets.jar_source_set import JarSourceSet

from pants_test.base_test import BaseTest


class JarSourceSetTest(BaseTest):

  def setUp(self):
    super(JarSourceSetTest, self).setUp()
    self.build_file_parser._build_configuration.register_target_alias('jar_source_set', JarSourceSet)
    self.build_file_parser._build_configuration.register_target_alias('jar_library', JarLibrary)
    self.build_file_parser._build_configuration.register_exposed_object('jar', JarDependency)

  def test_empty_imports(self):
    self.add_to_build_file('BUILD', dedent('''
    jar_source_set(name='foo',
    )'''))
    with self.assertRaises(JarSourceSet.ExpectedImportsError):
      self.build_graph.inject_spec_closure('//:foo')


  def test_simple(self):
    self.add_to_build_file('BUILD', dedent('''
    jar_source_set(name='foo',
      imports=[':import_jars'],
    )
    jar_library(name='import_jars',
      jars=[
        jar(org='foo', name='bar', rev='123'),
      ],
    )
   '''))

    self.build_graph.inject_spec_closure('//:foo')
    target = self.build_graph.get_target(SyntheticAddress.parse('//:foo'))
    self.assertIsInstance(target, JarSourceSet)
    traversable_specs = [spec for spec in target.traversable_specs]
    self.assertSequenceEqual([':import_jars'], traversable_specs)
    self.assertEquals(1, len(target.imports))
    import_jar_dep = target.imports[0]
    self.assertIsInstance(import_jar_dep, JarDependency)
