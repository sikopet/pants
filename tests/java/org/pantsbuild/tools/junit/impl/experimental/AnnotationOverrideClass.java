package org.pantsbuild.tools.junit.impl.experimental;

import org.pantsbuild.junit.annotations.TestParallel;
import org.pantsbuild.junit.annotations.TestParallelBoth;
import org.pantsbuild.junit.annotations.TestParallelMethods;
import org.pantsbuild.junit.annotations.TestSerial;

@TestSerial
@TestParallel
@TestParallelMethods
@TestParallelBoth
public class AnnotationOverrideClass {
}
