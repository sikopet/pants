package org.pantsbuild.tools.junit.impl.experimental;

import com.google.common.collect.ImmutableList;
import java.util.Set;
import org.junit.Test;
import org.pantsbuild.tools.junit.impl.Concurrency;

import static org.junit.Assert.assertEquals;

/**
 * Created by zundel on 5/2/16.
 */
public class SpecSetTest {

  @Test public void testExtractClasses() {
    // Not annotated
    Spec dummyClassSpec = new Spec(UnannotatedTestClass.class);
    // Annotated with PARALLEL_SERIAL
    Spec annotationOverrideSpec = new Spec(AnnotationOverrideClass.class);
    // Annotated with PARALLEL_BOTH
    Spec parallelBothSpec = new Spec(ParallelBothAnnotatedClass.class);

    SpecSet specSet = new SpecSet(
        ImmutableList.of(dummyClassSpec, annotationOverrideSpec, parallelBothSpec),
        Concurrency.PARALLEL_CLASSES);

    assertEquals(3, specSet.remaining().size());
    Class<?>[] parallelBothClasses = specSet.extractClasses(Concurrency.PARALLEL_BOTH);
    assertEquals(1, parallelBothClasses.length);
    assertEquals(ParallelBothAnnotatedClass.class, parallelBothClasses[0]);
    assertEquals(2, specSet.remaining().size());

    assertEquals(0, specSet.extractClasses(Concurrency.PARALLEL_METHODS).length);
    assertEquals(2, specSet.remaining().size());

    Class<?>[] parallelClassClasses = specSet.extractClasses(Concurrency.PARALLEL_CLASSES);
    assertEquals(1, parallelClassClasses.length);
    assertEquals(UnannotatedTestClass.class, parallelClassClasses[0]);

    Set<Spec> remaining = specSet.remaining();
    assertEquals(1, remaining.size());
    Spec remainingSpec = remaining.iterator().next();
    assertEquals(AnnotationOverrideClass.class, remainingSpec.getSpecClass());
  }
}
