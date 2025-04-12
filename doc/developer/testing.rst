.. SPDX-FileCopyrightText: 2024 Jani Nikula <jani@nikula.org>
.. SPDX-License-Identifier: BSD-2-Clause

.. _testing:

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

* ``test_extension_text()`` and ``test_extension_html()`` in
  ``test_extension.py``

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
cases. Each test case is defined by a ``.yaml`` file. The ``.yaml`` defines the
configuration, the input C or C++ source file, the expected reStructuredText
output file, and optionally a diagnostics (error messages) output file.

The YAML is parsed using StrictYAML, using a schema defined in ``testenv.py``.

The test approach, the relative path and the basename of the ``.yaml`` file
define the parametrized test case name in ``pytest``, for example
``test_parser[c/struct]``.

Test Cases as Examples
----------------------

The examples in the documentation are generated from test cases under the
``examples`` subdirectory, ensuring the examples actually work.

``make update-examples`` runs ``update_examples.py`` to generate
``doc/examples.rst`` from the example test cases.

Running
-------

Run tests using ``make test``. This calls ``pytest``. The ``pytest-xdist``
plugin parallelizes test execution.

Running individual test approaches, for examples ``test_parser``::

  $ pytest -k test_parser

Run individual test cases, for example ``c/struct``::

  $ pytest -k c/struct

Combined, with verbose output, for example::

  $ pytest -v -k test_cli[c/struct]
