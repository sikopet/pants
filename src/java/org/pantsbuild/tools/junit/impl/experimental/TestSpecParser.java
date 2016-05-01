package org.pantsbuild.tools.junit.impl.experimental;

import com.google.common.collect.ImmutableList;
import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * Takes strings passed to the command line representing packages or individual methods
 * and returns a parsed TestSpec.  Each TestSpec represents a single class, so individual methods
 * are added into each spec
 */
public class TestSpecParser {
  private final Iterable<String> testSpecStrings;
  private Map<Class<?>, TestSpec> specs = new HashMap<Class<?>, TestSpec>();

  /**
   * Parses the list of incoming test specs from the command line.
   * <p>
   * Expects a list of string specs which can be represented as one of:
   * <ul>
   *   <li>package.className</li>
   *   <li>package.className#methodName</li>
   * </ul>
   * Note that each class or method will only be executed once, no matter how many times it is
   * present in the list.
   * </p>
   * <p>
   * It is illegal to pass a spec with just the className if there are also individual methods
   * present in the list within the same class.
   * </p>
   */
  // TODO(zundel): This could easily be extended to allow a regular expression in the spec
  public TestSpecParser(Iterable<String> testSpecStrings) {
    this.testSpecStrings = testSpecStrings;
  }

  /**
   * Parse the specs passed in to the constructor.
   * @return List of parsed specs
   * @throws TestSpecException
   */
  public List<TestSpec> parse() throws TestSpecException {
    for (String specString : testSpecStrings) {
      if (specString.contains("#")) {
        addMethod(specString);
      } else {
        // The spec name is expected to be the same as the fully qualified class name
        if (specs.containsKey(specString)) {
          TestSpec spec = getOrCreateSpec(specString, specString);
          if (!spec.getMethods().isEmpty()) {
            throw new TestSpecException(specString,
                "Request for entire class already requesting individual methods");
          }
        } else {
          getOrCreateSpec(specString, specString);
        }
      }
    }
    return ImmutableList.copyOf(specs.values());
  }

  private TestSpec getOrCreateSpec(String specString, String className) throws TestSpecException {
    try {
      Class<?> clazz = getClass().getClassLoader().loadClass(className);
      return new TestSpec(clazz);
    } catch (ClassNotFoundException e) {
      throw new TestSpecException(specString,
          "Class %s not found in classpath.".format(className), e);
    }
  }

  /**
   * Handle a spec that looks like package.className#methodName
   */
  public void addMethod(String specString) throws TestSpecException {
    String[] results = specString.split("#");
    if (results.length != 2) {
      throw new TestSpecException(specString, "Expected only one # in spec");
    }
    String className = results[0];
    String methodName = results[1];

    TestSpec spec = getOrCreateSpec(specString, className);
    boolean found = false;
    for (Method clazzMethod : spec.getSpecClass().getMethods()) {
      if (clazzMethod.getName().equals(methodName)) {
        found = true;
        break;
      }
    }
    if (!found) {
      throw new TestSpecException(specString,
          "Method %s not found in class %s".format(methodName, className));
    }
    spec.addMethod(methodName);
  }
}
