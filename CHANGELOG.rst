Changelog
=========

Unreleased `master`_
--------------------

:Date: YYYY-MM-DD

Fixed
~~~~~

* Fix handling of anonymous enums, structs and unions for Clang 13

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

.. _master: https://github.com/jnikula/hawkmoth/compare/v0.10.0..master
.. _0.10.0: https://github.com/jnikula/hawkmoth/compare/v0.9.0..v0.10.0
.. _0.9.0: https://github.com/jnikula/hawkmoth/compare/v0.8.0..v0.9.0
.. _0.8.0: https://github.com/jnikula/hawkmoth/compare/v0.7.0..v0.8.0
.. _0.7.0: https://github.com/jnikula/hawkmoth/compare/v0.6..v0.7.0
.. _0.6: https://github.com/jnikula/hawkmoth/compare/v0.5..v0.6
.. _0.5: https://github.com/jnikula/hawkmoth/compare/v0.4..v0.5
.. _0.4: https://github.com/jnikula/hawkmoth/compare/v0.3..v0.4
.. _0.3: https://github.com/jnikula/hawkmoth/compare/v0.2..v0.3
.. _0.2: https://github.com/jnikula/hawkmoth/compare/1105c87c1078..v0.2
