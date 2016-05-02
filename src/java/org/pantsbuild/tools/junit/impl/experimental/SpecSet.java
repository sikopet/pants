package org.pantsbuild.tools.junit.impl.experimental;

import com.google.common.collect.ImmutableSet;
import java.util.Collection;
import java.util.LinkedHashSet;
import java.util.Set;
import org.pantsbuild.tools.junit.impl.Concurrency;


public class SpecSet {
  private final Set<Spec> remaining;
  private final Concurrency defaultConcurrency;

  public SpecSet(Collection<Spec> allSpecs, Concurrency defaultConcurrency) {
    this.remaining = new LinkedHashSet(allSpecs);
    this.defaultConcurrency = defaultConcurrency;
  }
  
  /**
   * Return all specs that match the specfied Concurrency parameter and have no separate test 
   * methods defined.
   */
  public Class<?>[] extractClasses(Concurrency concurrencyFilter) {
    Set<Spec> results = new LinkedHashSet<Spec>();
    for (Spec spec : remaining) {
      if (spec.getMethods().isEmpty() && 
          spec.getConcurrency(defaultConcurrency).equals(concurrencyFilter)) {
        results.add(spec);
      }
    }
    remaining.removeAll(results);
    
    Class<?>[] classes = new Class<?>[results.size()];
    int index = 0;
    for (Spec spec: results) {
     classes[index++] = spec.getSpecClass(); 
    }
    return classes;
  }
  
  public Set<Spec> remaining() {
    return ImmutableSet.copyOf(remaining);
  }

}