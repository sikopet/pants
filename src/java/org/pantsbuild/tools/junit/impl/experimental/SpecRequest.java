package org.pantsbuild.tools.junit.impl.experimental;

import java.io.PrintStream;
import org.junit.internal.requests.ClassRequest;
import org.junit.runner.Runner;
import org.pantsbuild.tools.junit.withretry.AllDefaultPossibilitiesBuilderWithRetry;

public class SpecRequest extends ClassRequest {
  private final Spec spec;
  private final int numRetries;
  private final PrintStream err;

  /**
   * Constructs an instance for the given test class, number of retries for failing tests
   * (0 means no retries) and a stream to print the information about flaky tests (those
   * that first fail but then pass after retrying).
   */
  public SpecRequest(Spec spec, int numRetries, PrintStream err) {
    super(spec.getSpecClass());
    this.spec = spec;
    this.numRetries = numRetries;
    this.err = err;
  }

  @Override
  public Runner getRunner() {
    return new AllDefaultPossibilitiesBuilderWithRetry(numRetries, err)
        .safeRunnerForClass(spec.getSpecClass());
  }
}
