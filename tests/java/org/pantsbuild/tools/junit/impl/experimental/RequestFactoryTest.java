package org.pantsbuild.tools.junit.impl.experimental;

import com.google.common.collect.ImmutableList;
import java.util.List;
import org.junit.Test;
import org.junit.internal.requests.FilterRequest;
import org.junit.runner.Request;

import static junit.framework.TestCase.assertTrue;
import static org.junit.Assert.assertEquals;

/**
 * Created by zundel on 5/2/16.
 */
public class RequestFactoryTest {

  @Test public void testClassRequest() {
    List<Spec> specs = ImmutableList.of(new Spec(UnannotatedTestClass.class));
    List<Request> requests = new RequestFactory().createRequests(specs, 0, System.err);
    assertEquals(1, requests.size());
    assertTrue(requests.get(0) instanceof SpecRequest);
  }

  @Test public void testMethodRequest() {
    Spec methodSpec = new Spec(UnannotatedTestClass.class);
    methodSpec.addMethod("testMethod");
    List<Spec> specs = ImmutableList.of(methodSpec);
    List<Request> requests = new RequestFactory().createRequests(specs, 0, System.err);
    assertEquals(1, requests.size());
    assertTrue(requests.get(0) instanceof FilterRequest);
  }
}
