package org.pantsbuild.tools.junit.impl.experimental;

import com.google.common.collect.ImmutableList;
import org.junit.Test;
import org.pantsbuild.junit.annotations.TestParallel;
import org.pantsbuild.junit.annotations.TestParallelBoth;
import org.pantsbuild.junit.annotations.TestParallelMethods;
import org.pantsbuild.junit.annotations.TestSerial;
import org.pantsbuild.tools.junit.impl.Concurrency;

import static org.junit.Assert.assertEquals;

public class SpecTest {

  @Test public void testAddMethod() throws Exception {
    Spec spec = new Spec(DummyClass.class);
    assertEquals(DummyClass.class, spec.getSpecClass());
    assertEquals("org.pantsbuild.tools.junit.impl.experimental.SpecTest$DummyClass", spec.getSpecName());
    assertEquals(ImmutableList.of(), spec.getMethods());
    spec.addMethod("testMethod");
    assertEquals(ImmutableList.of("testMethod"), spec.getMethods());
    spec.addMethod("foo");
    assertEquals(ImmutableList.of("testMethod", "foo"), spec.getMethods());
  }

  @Test public void testDefaultConcurrency() {
    Spec spec = new Spec(DummyClass.class);
    assertEquals(Concurrency.SERIAL, spec.getConcurrency(Concurrency.SERIAL));
    assertEquals(Concurrency.PARALLEL_CLASSES, spec.getConcurrency(Concurrency.PARALLEL_CLASSES));
    assertEquals(Concurrency.PARALLEL_METHODS, spec.getConcurrency(Concurrency.PARALLEL_METHODS));
    assertEquals(Concurrency.PARALLEL_BOTH, spec.getConcurrency(Concurrency.PARALLEL_BOTH));
  }

  @Test public void testAnnotatedConcurrency() {
    Spec spec = new Spec(ParallelBothClass.class);
    assertEquals(Concurrency.PARALLEL_BOTH, spec.getConcurrency(Concurrency.SERIAL));
    assertEquals(Concurrency.PARALLEL_BOTH, spec.getConcurrency(Concurrency.PARALLEL_METHODS));
  }

  @Test public void testAnnotationPrecedence() {
    Spec spec = new Spec(AnnotationOverrideClass.class);
    assertEquals(Concurrency.SERIAL, spec.getConcurrency(Concurrency.PARALLEL_BOTH));
  }
}
