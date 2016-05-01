package org.pantsbuild.tools.junit.impl.experimental;

import java.util.LinkedHashSet;
import java.util.List;
import java.util.Set;
import org.pantsbuild.tools.junit.impl.Concurrency;


public class SpecFilter {

  /**
   * Return all specs that match the specfied Concurrency parameter.
   */
  public static Set<Spec> filterConcurrency(Set<Spec> specs, Concurrency concurrencyFilter,
      Concurrency defaultConcurrency) {
    Set<Spec> results = new LinkedHashSet<Spec>();
    for (Spec spec : specs) {
      if (spec.getConcurrency(defaultConcurrency).equals(concurrencyFilter)) {
        results.add(spec);
      }
    }
    return results;
  }

  /**
   * Return all specs with no methods defined.
   */
  public static Set<Spec> filterNoMethods(Set<Spec> specs) {
    Set<Spec> results = new LinkedHashSet<Spec>();
    for (Spec spec : specs) {
      if (spec.getMethods().size() == 0) {
        results.add(spec);
      }
    }
    return results;
  }

  // Utility class, do not instantiate
  private SpecFilter() {
  }
}