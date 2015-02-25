# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

# Like Hello World, but built with Pants.

jvm_app(name='rb1761',
  basename = 'rb1761-example',
  dependencies = [
    ':hello-main',
  ],
)

# The binary, the "runnable" part:

jvm_binary(name = 'hello-main',
  source = 'HelloMain.java',
  main = 'com.pants.examples.rb1761.HelloMain',
)


jvm_binary(name = 'undeclared-dep-main',
  source = 'UndeclaredDepMain.java',
  main = 'com.pants.examples.rb1761.UndeclaredDepMain',
  dependencies = [
    ':undeclared-dep-lib',
  ]
)

java_library(name='undeclared-dep-lib',
  sources=['UndeclaredDepLib.java'],
  dependencies = [
  ],
)

java_library(name='declared-dep-lib',
  sources=['DeclaredDepLib.java'],
  dependencies = [
   '3rdparty:guava',
  ],
)




