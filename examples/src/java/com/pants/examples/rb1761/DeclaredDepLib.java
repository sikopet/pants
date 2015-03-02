package com.pants.examples.rb1761;

import com.google.common.collect.ImmutableList;
import java.util.List;

public class DeclaredDepLib {

  public List<String> foo() {
    return ImmutableList.<String>of("a", "b", "c");
  }
}
