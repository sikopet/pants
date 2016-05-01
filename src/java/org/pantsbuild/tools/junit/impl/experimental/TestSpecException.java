package org.pantsbuild.tools.junit.impl.experimental;

public class TestSpecException extends Exception {

  public TestSpecException(String spec, String message) {
    super(formatMessage(spec, message));
  }

  public TestSpecException(String spec, String message, Throwable t) {
    super(formatMessage(spec, message), t);
  }

  private static String formatMessage(String spec, String message) {
    return "FATAL: Error parsing spec %s: %s".format(spec, message);
  }
}
