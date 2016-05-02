package org.pantsbuild.tools.junit.impl.experimental;

import org.junit.runner.Description;
import org.junit.runner.manipulation.Filter;

public class SpecFilter extends Filter {
  private final Spec spec;

  public SpecFilter(Spec spec) {
    this.spec = spec;
  }

  @Override public boolean shouldRun(Description description) {
    if (spec.getMethods().isEmpty()) {
      return true;
    }

    for (String method : spec.getMethods()) {
      if (Description.createTestDescription(spec.getSpecClass(), method).equals(description)) {
        return true;
      }
    }
    return false;
  }

  @Override public String describe() {
    return "Filters using a Spec";
  }
}
