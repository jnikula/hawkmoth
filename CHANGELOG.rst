.. SPDX-FileCopyrightText: 2021 Jani Nikula <jani@nikula.org>
.. SPDX-License-Identifier: BSD-2-Clause

Changelog
=========

Unreleased `master`_
--------------------

:Date: YYYY-MM-DD

Added
~~~~~

* Better support for documenting typedefs of function pointers
* CI checks for `REUSE compliance`_.

.. _REUSE compliance: https://reuse.software/

Changed
~~~~~~~

* Switched to ``SPDX-FileCopyrightText`` and ``SPDX-License-Identifier``
  copyright and license headers

Fixed
~~~~~

* Parsed file lookups when ``:clang:`` option is being used (#273)

Hawkmoth `0.20.0`_
------------------

:Date: 2025-04-03

Added
~~~~~

* Automatic configuration of system header search paths, enabled by default, and
  configurable via ``hawkmoth_autoconf`` option
* ``hawkmoth_compiler`` option to set the compiler for autoconf
* CI on macOS
* Dockerfile for testing on Arch Linux

Deprecated
~~~~~~~~~~

* Direct use of ``compiler.get_include_args()`` in favour of ``hawkmoth_autoconf``

Hawkmoth `0.19.0`_
------------------

:Date: 2024-10-26

Added
~~~~~

* Support for C++ namespaces
* Domain specific config options ``hawkmoth_clang_c`` and
  ``hawkmoth_clang_cpp``.

Changed
~~~~~~~

* Bumped Python dependency requirement to v3.9, as v3.8 is reaching end of life
* The ``hawkmoth.ext.transformations`` extension is no longer loaded
  automatically as it has been deprecated
* Moved developer documentation under doc/developer/
* Switched from ``setup.cfg`` to ``pyproject.toml``
* Switched build backend to hatchling

Deprecated
~~~~~~~~~~

* The ``hawkmoth.ext.transformations`` extension and the
  ``hawkmoth.util.doccompat`` module in favour of the ``hawkmoth.ext.javadoc``
  and ``hawkmoth.ext.napoleon`` extensions and the
  ``hawkmoth-process-docstring`` event.

Removed
~~~~~~~

* ``hawkmoth --compat={none,javadoc-basic,javadoc-liberal,kernel-doc}`` option
  from CLI
* ``cautodoc_root`` configuration option in favour of ``hawkmoth_root``
* ``cautodoc_clang`` configuration option in favour of ``hawkmoth_clang``

Hawkmoth `0.18.0`_
------------------

:Date: 2024-04-14

Added
~~~~~

* Added support for documenting C++ alias type definitions
* Added support variadic macros with named variable argument

Changed
~~~~~~~

* Bumped Python dependency requirement to v3.8, as the earlier versions have
  reached end of life

Fixed
~~~~~

* Fixed C++ ``extern "C"`` block parsing for Clang 18 and later

Hawkmoth `0.17.0`_
------------------

:Date: 2023-12-10

Added
~~~~~

* Considerably improved Javadoc/Doxygen support
* Started making GitHub releases
* Support for adding automated source links
* Tips and tricks documentation
* ``hawkmoth --version`` option to CLI
* ``hawkmoth --process-docstring={javadoc,napoleon}`` option to CLI

Changed
~~~~~~~

* Switched from CRITICAL to ERROR level for Sphinx errors
* Internally, refactored cursor handling

Fixed
~~~~~

* Clang language option to handle headers better
* Line number references in error messages
* Referencing typedefed anonymous structs, unions, and enums on Clang 15 and earlier

Hawkmoth `0.16.0`_
------------------

:Date: 2023-10-22

Added
~~~~~

* Normalization of _Bool to bool
* Symbolic dimensions to array documentation
* Dockerfiles for running tests in more distros

Changed
~~~~~~~

* Naming of typedef anonymous struct/union/enum to use typedef name instead of
  generated ``@anonymous_*``

Fixed
~~~~~

* setup.cfg license_file deprecation warning
* Documentation intersphinx references to Sphinx documentation
* Test suite docutils warnings
* Test suite system include path for e.g. Fedora
* Handling of anonymous struct/union/enum with libclang v16 and later
* Workaround libclang tokenization issue
* Running test suite with plain ``pytest`` in root directory

Hawkmoth `0.15.0`_
------------------

:Date: 2023-08-17

Added
~~~~~

* ``autosection`` directive to include generic documentation comments
* ``.readthedocs.yaml`` config file
* Documentation on how to use Hawkmoth on Read the Docs more reliably
* Values in enumerator documentation when explicitly initialized in source code

Changed
~~~~~~~

* The ``:file:`` option is optional for files that have been previously parsed
* Test case yaml schema

Removed
~~~~~~~

* Development dependency on the deprecated ``sphinx_testing`` package
* Docker containers

Fixed
~~~~~

* Handling of empty documentation comments
* Parser error propagation

Hawkmoth `0.14.0`_
------------------

:Date: 2023-04-01

Added
~~~~~

* Build and deploy stable and development documentation at GitHub pages

Changed
~~~~~~~

* Switch the project to src/ hierarchy
* Test the installed package instead of source to detect packaging issues
* Require functional hawkmoth to build documentation

Removed
~~~~~~~

* Sunset the mailing list as contact

Fixed
~~~~~

* Fix packaging of hawkmoth.ext.* sub-packages

Hawkmoth `0.13.0`_
------------------

:Date: 2023-03-21

Added
~~~~~

* Early support for documenting C++ (contributions courtesy of `Critical Software`_)
* Support for extending documentation comment parsing and transformations via
  ``hawkmoth-process-docstring`` event
* ``hawkmoth_transform_default`` configuration option for the
  ``hawkmoth-process-docstring`` event
* ``hawkmoth_root`` configuration option to replace ``cautodoc_root``
* ``hawkmoth_clang`` configuration option to replace ``cautodoc_clang``
* Built-in extensions for Javadoc and Napoleon comment handling

.. _Critical Software: https://www.criticalsoftware.com/

Changed
~~~~~~~

* Typedefed anonymous struct, union, and enum parsing to be more explicit
* ``cautodoc_transformations`` handling moved to a built-in extension
* Lots of test suite refactoring and cleanups

Deprecated
~~~~~~~~~~

* ``cautodoc_root`` configuration option in favour of ``hawkmoth_root``
* ``cautodoc_clang`` configuration option in favour of ``hawkmoth_clang``

Removed
~~~~~~~

* ``cautodoc_compat`` configuration option
* ``compat`` directive option

Hawkmoth `0.12.0`_
------------------

:Date: 2022-12-13

Added
~~~~~

* Parsing for function pointer argument names
* Guide to contributing
* Troubleshooting documentation
* Install 'hawkmoth' command-line tool for debugging
* GitHub CI automation
* Overview documentation for the tests

Changed
~~~~~~~

* Log Clang and parser warnings at default Sphinx verbosity level
* Bumped Docker container Sphinx version to 5.3.0
* Cleaned up examples section of the documentation

Fixed
~~~~~

* Fix whitespace in the output
* Fix function definitions with void parameter list as opposed to empty
* Fix parser warnings on documentation comments in unexpected locations
* Fix Clang warnings from examples in 'make html'

Hawkmoth `0.11.0`_
------------------

:Date: 2022-04-03

Fixed
~~~~~

* Fix handling of anonymous enums, structs and unions for Clang 13
* Fix handling of arrays of pointers

Hawkmoth `0.10.0`_
------------------

:Date: 2021-10-30

Changed
~~~~~~~

* More internal testing refactoring
* Use flake8 to enforce style

Fixed
~~~~~

* Fix handling of anonymous enums, structs and unions

Hawkmoth `0.9.0`_
-----------------

:Date: 2021-09-30

Added
~~~~~

* New fine-grained documentation directives ``c:autovar``, ``c:autotype``,
  ``c:automacro``, ``c:autofunction``, ``c:autostruct``, ``c:autounion``, and
  ``c:autoenum``
* Dockerfiles for Docker Hub container images

Changed
~~~~~~~

* Major internal implementation and testing refactoring
* IRC channel moved to OFTC IRC network

Fixed
~~~~~

* Documentation comment line prefix/indent removal (#64)
* Hawkmoth documentation on Read the Docs

Hawkmoth `0.8.0`_
-----------------

:Date: 2021-05-21

Added
~~~~~

* Helper for discovering and configuring system include path
* Transform functionality for comment conversion

Changed
~~~~~~~

* Extension ``cautodoc_clang`` configuration option must now be a Python list
* Directive ``clang`` option now extends instead of overrides ``cautodoc_clang``
* Bumped Python dependency requirement to v3.6 for f-strings
* Switched to pytest for testing
* Switched to static packaging metadata
* Deprecated compat functionality in favour of transformations

Fixed
~~~~~

* Array function parameter documentation
* Function pointers with qualifiers such as const

Hawkmoth `0.7.0`_
-----------------

:Date: 2021-01-29

Added
~~~~~

* Retroactively written changelog
* Helper and documentation for using Hawkmoth on Read the Docs

Changed
~~~~~~~

* Switched to semantic versioning

Fixed
~~~~~

* Array member documentation in structs and unions
* Function pointer documentation
* Clang diagnostics without a file; e.g. on command-line parameter errors

Hawkmoth `0.6`_
---------------

:Date: 2020-12-30

Added
~~~~~

* Support for Sphinx v3.0 and later
* Use new Sphinx features for macro, struct, union, enum and enumerator
  documentation
* Detailed installation instructions
* Simple Dockerfile for testing
* requirements.txt and virtual environment helper

Changed
~~~~~~~

* General documentation improvements
* Fallback code for documentation builds without Hawkmoth

Removed
~~~~~~~

* Sphinx v1.x and v2.x support

Fixed
~~~~~

* Array variable documentation

Hawkmoth `0.5`_
---------------

:Date: 2020-01-25

Changed
~~~~~~~

* Bumped development status to beta
* Improved macro documentation test cases
* Improved function documentation test cases

Deprecated
~~~~~~~~~~

* Last version to support Sphinx versions v1.x and v2.x.

Fixed
~~~~~

* Documentation of non-prototyped functions

Hawkmoth `0.4`_
---------------

:Date: 2019-06-08

Added
~~~~~

* Support for propagating Clang diagnostics to Sphinx

Changed
~~~~~~~

* Rename hawkmoth parser module
* Testing updates

Hawkmoth `0.3`_
---------------

:Date: 2019-01-29

Changed
~~~~~~~

* Python packaging update
* Testing updates

Hawkmoth `0.2`_
---------------

:Date: 2019-01-26

Added
~~~~~

* Python packaging
* Support for variadic function documentation
* Support for variadic macro documentation

Changed
~~~~~~~

* Parser refactoring
* Testing overhaul, switch to sphinx_testing

.. _master: https://github.com/jnikula/hawkmoth/compare/v0.20.0..master
.. _0.20.0: https://github.com/jnikula/hawkmoth/compare/v0.19.0..v0.20.0
.. _0.19.0: https://github.com/jnikula/hawkmoth/compare/v0.18.0..v0.19.0
.. _0.18.0: https://github.com/jnikula/hawkmoth/compare/v0.17.0..v0.18.0
.. _0.17.0: https://github.com/jnikula/hawkmoth/compare/v0.16.0..v0.17.0
.. _0.16.0: https://github.com/jnikula/hawkmoth/compare/v0.15.0..v0.16.0
.. _0.15.0: https://github.com/jnikula/hawkmoth/compare/v0.14.0..v0.15.0
.. _0.14.0: https://github.com/jnikula/hawkmoth/compare/v0.13.0..v0.14.0
.. _0.13.0: https://github.com/jnikula/hawkmoth/compare/v0.12.0..v0.13.0
.. _0.12.0: https://github.com/jnikula/hawkmoth/compare/v0.11.0..v0.12.0
.. _0.11.0: https://github.com/jnikula/hawkmoth/compare/v0.10.0..v0.11.0
.. _0.10.0: https://github.com/jnikula/hawkmoth/compare/v0.9.0..v0.10.0
.. _0.9.0: https://github.com/jnikula/hawkmoth/compare/v0.8.0..v0.9.0
.. _0.8.0: https://github.com/jnikula/hawkmoth/compare/v0.7.0..v0.8.0
.. _0.7.0: https://github.com/jnikula/hawkmoth/compare/v0.6..v0.7.0
.. _0.6: https://github.com/jnikula/hawkmoth/compare/v0.5..v0.6
.. _0.5: https://github.com/jnikula/hawkmoth/compare/v0.4..v0.5
.. _0.4: https://github.com/jnikula/hawkmoth/compare/v0.3..v0.4
.. _0.3: https://github.com/jnikula/hawkmoth/compare/v0.2..v0.3
.. _0.2: https://github.com/jnikula/hawkmoth/compare/1105c87c1078..v0.2
