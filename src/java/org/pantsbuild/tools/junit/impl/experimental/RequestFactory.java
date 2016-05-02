package org.pantsbuild.tools.junit.impl.experimental;

import java.io.PrintStream;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import org.junit.runner.Request;

public class RequestFactory {
  public List<Request> createRequests(Collection<Spec> specs, int numRetries, PrintStream err) {
    List<Request> requests = new ArrayList<Request>();
    for (Spec spec: specs) {
      Request request = new SpecRequest(spec, numRetries, err);
      if (!spec.getMethods().isEmpty()) {
        request = request.filterWith(new SpecFilter(spec));
      }
      requests.add(request);
    }
    return requests;
  }
}
