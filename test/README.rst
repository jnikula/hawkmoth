Testing
=======

This is a brief description of the approach to testing.

The main idea is to compare documentation comments extracted from source to
predefined, expected reStructuredText output.

Test Files and Functions
------------------------

There are three test files, with different levels and approaches, run by
``pytest``:

* ``test_parser()`` in ``test_parser.py``

  Test the parser directly. The documentation comments are extracted through the
  parser Python interface.

* ``test_cli()`` in ``test_cli.py``

  Test the parser and the command-line interface. The documentation comments are
  extracted through the command-line interface.

* ``test_text()`` and ``test_html()`` in ``test_cautodoc.py``

  Test the parser and the Sphinx extension, using two builders: text and
  html. The documentation comments are extracted through the Sphinx build
  process, running the extension.

The above test functions are parametrized to be run for each test case (see
below).

Each test file contains abstractions depending on the approach, calling the
generic ``run_test()`` function in ``testenv.py``, making the test files and
functions just a thin glue layer.

Test Cases
----------

The test functions described above are parametrized using what we call test
cases. Each test case is defined by a pair of ``.yaml`` and ``.rst`` files. The
``.yaml`` defines the configuration and the input C source file, while the
``.rst`` is the expected output. Optionally a ``.stderr`` file can define the
expected error output.

The YAML is parsed using StrictYAML, using a schema defined in ``testenv.py``.

The basename of the ``.yaml`` file becomes the parametrized test case name in
``pytest``.

Test Cases as Examples
----------------------

The examples in the documentation are generated from test cases named
``example-*``, ensuring the examples actually work.

``make update-examples`` runs ``update-examples.py`` to generate
``doc/examples.rst``.

Running
-------

Run tests using ``make test``. This calls ``pytest``. The ``pytest-xdist``
plugin parallelizes test execution.

Running individual test approaches, for examples ``test_parser``::

  $ pytest -k test_parser test

Run individual test cases, for example ``struct``::

  $ pytest -k [struct] test

Combined, with verbose output, for example::

  $ pytest -v -k test_cli[struct] test
