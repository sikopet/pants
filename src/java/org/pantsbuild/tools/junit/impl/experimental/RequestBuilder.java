package org.pantsbuild.tools.junit.impl.experimental;

import com.google.common.collect.ImmutableList;
import java.util.List;
import org.junit.runner.Request;

public class RequestBuilder {
  public RequestBuilder(boolean perTestTimer, int testShard, int numTestShards, int numRetries) {
  }

  public List<Request> createRequests(List<Spec> specs) {
    return ImmutableList.of();
  }
}
