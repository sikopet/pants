# coding=utf-8
# Copyright 2015 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

from pants.ivy.bootstrapper import Bootstrapper

from pants_test.base_test import BaseTest


class BootstrapperTest(BaseTest):

  def test_parse_proxy_string(self):
    bootstrapper = Bootstrapper().instance()

    self.assertEquals(('example.com', '1234'),
                      bootstrapper._parse_proxy_string("http://example.com:1234"))
    self.assertEquals(('secure-example.com', '999'),
                      bootstrapper._parse_proxy_string("http://secure-example.com:999"))
    # trailing slash is ok
    self.assertEquals(('example.com', '1234'),
                      bootstrapper._parse_proxy_string("http://example.com:1234/"))
