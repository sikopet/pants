# Copyright 2014 Pants project contributors (see CONTRIBUTORS.md).
# Licensed under the Apache License, Version 2.0 (see LICENSE).

python_library(
  name = 'task_registrar',
  sources = ['task_registrar.py'],
  dependencies = [
    ':error',
    ':goal',
    'src/python/pants/backend/core/tasks:task',
  ],
)

python_library(
  name = 'aggregated_timings',
  sources = ['aggregated_timings.py'],
  dependencies = [
    'src/python/pants/util:dirutil',
  ]
)

# why is this in goal?
python_library(
  name = 'artifact_cache_stats',
  sources = ['artifact_cache_stats.py'],
  dependencies = [
    'src/python/pants/util:dirutil',
  ]
)

python_library(
  name = 'context',
  sources = ['context.py'],
  dependencies = [
    ':products',
    ':workspace',
    '3rdparty/python/twitter/commons:twitter.common.dirutil',
    '3rdparty/python/twitter/commons:twitter.common.process',
    'src/python/pants/base:address',
    'src/python/pants/base:build_environment',
    'src/python/pants/base:source_root',
    'src/python/pants/base:build_graph',
    'src/python/pants/base:target', # XXX(fixme)
    'src/python/pants/base:workunit',
    'src/python/pants/java:distribution',  # XXX(fixme)
    'src/python/pants/process',
    'src/python/pants/reporting',
  ],
)

python_library(
  name = 'error',
  sources = ['error.py'],
)

python_library(
  name = 'initialize_reporting',  # XXX shouldn't this be in reporting?!
  sources = ['initialize_reporting.py'],
  dependencies = [
    '3rdparty/python/twitter/commons:twitter.common.lang',
    'src/python/pants/reporting',
    'src/python/pants/util:dirutil',
  ],
)

python_library(
  name = 'option_helpers',
  sources = ['option_helpers.py'],
  dependencies = [
    'src/python/pants/base:config',
  ],
)

# TODO(benjy): As a result of a renaming, we ended up with this target owning only one source
# file, whereas its name might indicate to the casual reader that it represents the entire package.
# However the targets in this BUILD file (and elsewhere) are probably too fine-grained anyway, so
# we may just solve this possible confusion by refactoring out some stuff and unifying the rest.
python_library(
  name = 'goal',
  sources = ['goal.py'],
  dependencies = [
    ':error',
    ':mkflag',
  ],
)

python_library(
  name = 'mkflag',
  sources = ['mkflag.py'],
  dependencies = [
  ],
)

python_library(
  name = 'products',
  sources = ['products.py'],
  dependencies = [
    '3rdparty/python/twitter/commons:twitter.common.collections',
  ],
)

python_library(
  name = 'run_tracker',
  sources = ['run_tracker.py'],
  dependencies = [
    ':aggregated_timings',
    ':artifact_cache_stats',
    'src/python/pants/base:run_info',
    'src/python/pants/base:worker_pool',
    'src/python/pants/base:workunit',
    'src/python/pants/reporting', # XXX(fixme)
    'src/python/pants/base:config',
  ],
)

python_library(
  name = 'workspace',
  sources = ['workspace.py'],
  dependencies = [
    '3rdparty/python/twitter/commons:twitter.common.lang',
    'src/python/pants/base:build_environment',
    'src/python/pants/scm',
  ],
)
