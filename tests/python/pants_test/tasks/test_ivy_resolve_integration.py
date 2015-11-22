# coding=utf-8
# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from __future__ import (absolute_import, division, generators, nested_scopes, print_function,
                        unicode_literals, with_statement)

import os
import re

from pants_test.pants_run_integration_test import PantsRunIntegrationTest, ensure_cached


class IvyResolveIntegrationTest(PantsRunIntegrationTest):

  def test_ivy_resolve_gives_correct_exception_on_cycles(self):
    with self.temporary_workdir() as workdir:
      pants_run = self.run_pants_with_workdir([
          'compile', 'testprojects/src/java/org/pantsbuild/testproject/cycle1'], workdir)
      self.assert_failure(pants_run)
      self.assertIn('Cycle detected', pants_run.stderr_data)

  def test_java_compile_with_ivy_report(self):
    # Ensure the ivy report file gets generated
    with self.temporary_workdir() as workdir:
      ivy_report_dir = '{workdir}/ivy-report'.format(workdir=workdir)
      pants_run = self.run_pants_with_workdir([
          'compile',
          'testprojects/src/java/org/pantsbuild/testproject/unicode/main',
          '--resolve-ivy-report',
          '--resolve-ivy-outdir={reportdir}'.format(reportdir=ivy_report_dir)],
          workdir)
      self.assert_success(pants_run)

      # Find the ivy report
      found = False
      pattern = re.compile('internal-[a-f0-9]+-default\.html$')
      for f in os.listdir(ivy_report_dir):
        if os.path.isfile(os.path.join(ivy_report_dir, f)):
          if pattern.match(f):
            found = True
            break
      self.assertTrue(found,
                      msg="Couldn't find ivy report in {report_dir}"
                      .format(report_dir=ivy_report_dir))

  def test_ivy_args(self):
    pants_run = self.run_pants([
        'resolve',
        '--resolve-ivy-args=-blablabla',
        'examples/src/scala::'
    ])
    self.assert_failure(pants_run)
    self.assertIn('Unrecognized option: -blablabla', pants_run.stdout_data)

  def test_ivy_confs_success(self):
    pants_run = self.run_pants([
        'resolve',
        '--resolve-ivy-confs=default',
        '--resolve-ivy-confs=sources',
        '--resolve-ivy-confs=javadoc',
        '3rdparty:junit'
    ])
    self.assert_success(pants_run)

  def test_ivy_confs_failure(self):
    pants_run = self.run_pants([
        'resolve',
        '--resolve-ivy-confs=parampampam',
        '3rdparty:junit'
    ])
    self.assert_failure(pants_run)

  def test_ivy_confs_ini_failure(self):
    pants_ini_config = {'resolve.ivy': {'confs': 'parampampam'}}
    pants_run = self.run_pants([
        'resolve',
        '3rdparty:junit'
    ], config=pants_ini_config)
    self.assert_failure(pants_run)

  # NB(zundel): This test is a bit brittle in that it expects to know what the caching behavior
  # is like of other modules.  Expects 2 artifacts for ivy resolve, and 2 for compile.
  # Before https://rbcommons.com/s/twitter/r/3168 we saw an extra compile artifact created.
  @ensure_cached(expected_num_artifacts=4)
  def test_ivy_resolve_stable(self, cache_args):
    pants_run = self.run_pants([
      'compile',
      '--no-cache-compile-checkstyle-write',
      'testprojects/src/java/org/pantsbuild/testproject/inccompile/libwithjettydep',
      cache_args
    ])
    self.assert_success(pants_run)
    pants_run = self.run_pants([
      'compile',
      '--no-cache-compile-checkstyle-write',
      'testprojects/src/java/org/pantsbuild/testproject/inccompile/libwithjettyserver',
      cache_args
    ])
    self.assert_success(pants_run)
