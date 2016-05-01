package org.pantsbuild.tools.junit.impl.experimental;

import com.google.common.collect.ImmutableList;
import java.util.List;
import org.junit.runner.Request;
import org.pantsbuild.tools.junit.impl.experimental.TestSpec;


public class RequestBuilder {
  public RequestBuilder(boolean perTestTimer, int testShard, int numTestShards, int numRetries) {
  }

  public List<Request> createRequests(List<TestSpec> specs) {
    return ImmutableList.of();
  }
}
