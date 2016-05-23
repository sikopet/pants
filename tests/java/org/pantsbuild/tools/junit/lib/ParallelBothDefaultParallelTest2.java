// Copyright 2016 Pants project contributors (see CONTRIBUTORS.md).
// Licensed under the Apache License, Version 2.0 (see LICENSE).
package org.pantsbuild.tools.junit.lib;

import org.junit.Test;

/**
 * See {@link ParallelBothDefaultParallelTest1}
 */
public class ParallelBothDefaultParallelTest2 {

  @Test
  public void pbdptest21() throws Exception {
    ParallelBothDefaultParallelTest1.awaitLatch("pbdptest21");
  }

  @Test
  public void pbdptest22() throws Exception {
    ParallelBothDefaultParallelTest1.awaitLatch("pbdptest22");
  }
}
