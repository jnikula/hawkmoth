.. _contributing:

Contributing
============

Hey, thanks for your interest in contributing to Hawkmoth!

Here's some initial guidance to help you contribute, which is hopefully better
than nothing.

Broad Strokes
-------------

In short, keep it simple.

Simplicity applies both to the use and implementation of Hawkmoth. If a feature
gets complicated, it probably does not belong in Hawkmoth. There are big fancy
projects such as Doxygen and Breathe out there to comprehensively document C and
C++ projects in Sphinx, but they're complicated to use and understand.

Design Checklist
----------------

* Absolutely minimal parsing of the documentation comments.

Contribution Checklist
----------------------

* New or modified features need test coverage. Add or update the tests in the
  ``test`` directory accordingly. See `test/README.rst`_ for an overview of the
  approach to testing.

* Bug fixes need test coverage. Ideally add an expected failure test case
  demonstrating the bug first, and then fix it.

* Make sure the tests pass for every commit::

    make test

  or, to run the tests in a Docker container::

    make docker-test

* Make sure the static analysis (style checks, etc.) passes for every commit::

    make check

* User-visible changes need documentation.

* Make sure the documentation build passes for every commit::

    make html

.. _test/README.rst: https://github.com/jnikula/hawkmoth/blob/master/test/README.rst
