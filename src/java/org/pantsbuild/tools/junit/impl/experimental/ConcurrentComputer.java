package org.pantsbuild.tools.junit.impl.experimental;

import com.google.common.base.Preconditions;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import org.junit.runner.Computer;
import org.junit.runner.Runner;
import org.junit.runners.ParentRunner;
import org.junit.runners.model.InitializationError;
import org.junit.runners.model.RunnerBuilder;
import org.junit.runners.model.RunnerScheduler;
import org.pantsbuild.tools.junit.impl.Concurrency;


public class ConcurrentComputer extends Computer {
  private final Concurrency concurrency;
  private final int numParallelThreads;

  public ConcurrentComputer(Concurrency concurrency, int numParallelThreads) {
    Preconditions.checkNotNull(concurrency);
    this.concurrency = concurrency;
    this.numParallelThreads = numParallelThreads > 0 ? numParallelThreads : 1;
  }

  private Runner parallelize(Runner runner) {
    if (runner instanceof ParentRunner) {
      ((ParentRunner<?>) runner).setScheduler(new RunnerScheduler() {
        private final ExecutorService fService = Executors.newFixedThreadPool(numParallelThreads);

        public void schedule(Runnable childStatement) {
          fService.submit(childStatement);
        }

        public void finished() {
          try {
            fService.shutdown();
            // TODO(zundel): Change long wait?
            fService.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
          } catch (InterruptedException e) {
            e.printStackTrace(System.err);
          }
        }
      });
    }
    return runner;
  }

  @Override
  public Runner getSuite(RunnerBuilder builder, java.lang.Class<?>[] classes)
      throws InitializationError {
    Runner suite = super.getSuite(builder, classes);
    return this.concurrency.shouldRunClassesParallel() ? parallelize(suite) : suite;
  }

  @Override
  protected Runner getRunner(RunnerBuilder builder, Class<?> testClass)
      throws Throwable {
    Runner runner = super.getRunner(builder, testClass);
    return this.concurrency.shouldRunMethodsParallel() ? parallelize(runner) : runner;
  }
}
