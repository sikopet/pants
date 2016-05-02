package org.pantsbuild.tools.junit.impl.experimental;

import org.junit.Test;
import org.junit.runner.Description;

import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertFalse;

/**
 * Created by zundel on 5/2/16.
 */
public class SpecFilterTest {

  @Test public void testFilterNoMethods() {
    SpecFilter filter = new SpecFilter(new Spec(UnannotatedTestClass.class));
    // Any description should work
    assertTrue(filter.shouldRun(Description.EMPTY));
    assertTrue(filter.shouldRun(
        Description.createTestDescription(UnannotatedTestClass.class, "testMethod")));
    assertTrue(filter.shouldRun(
        Description.createTestDescription(UnannotatedTestClass.class, "foo")));
  }

  @Test public void testFilterMethods() {
    Spec spec = new Spec(UnannotatedTestClass.class);
    spec.addMethod("testMethod");
    SpecFilter filter = new SpecFilter(spec);
    assertTrue(filter.shouldRun(
        Description.createTestDescription(UnannotatedTestClass.class, "testMethod")));
    assertFalse(filter.shouldRun(
        Description.createTestDescription(UnannotatedTestClass.class, "foo")));
  }
}
