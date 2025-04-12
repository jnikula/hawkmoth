.. SPDX-FileCopyrightText: 2017 Jani Nikula <jani@nikula.org>
.. SPDX-License-Identifier: BSD-2-Clause

.. _syntax:

Syntax
======

For the :ref:`Hawkmoth autodoc directives <directives>` to work, the C or C++
source code must be documented using specific documentation comment style, and
the comments must follow reStructuredText markup.

Optionally, the syntax may be :ref:`extended <extending-the-syntax>` to support
e.g. Javadoc/Doxygen and Napoleon style comments.

See :ref:`the examples section <examples>` for a quick tour of what's possible,
and read on for documentation comment formatting details.

Documentation Comments
----------------------

Documentation comments are C/C++ language block comments that begin with
``/**``.

Because reStructuredText is sensitive about indentation, it's strongly
recommended, even if not strictly required, to follow a uniform style for
multi-line comments. Place the opening delimiter ``/**`` and closing delimiter
``␣*/`` on lines of their own, and prefix the lines in between with ``␣*␣``.
Indent the actual documentation at the third column, to let Hawkmoth
consistently remove the enclosing comment markers:

.. code-block:: c

  /**
   * The quick brown fox jumps
   * over the lazy dog.
   */

One-line comments are fine too:

.. code-block:: c

   /** The quick brown fox jumps over the lazy dog. */

All documentation comments preceding C or C++ constructs are attached to them,
and result in C or C++ Domain directives being added for them accordingly. This
includes macros, functions, struct and union members, enumerations, etc.

Documentation comments followed by comments (documentation or not) are included
as normal paragraphs in the order they appear.

Info Field Lists
----------------

Use reStructuredText `field lists`_ for documenting function parameters, return
values, and arbitrary other data. Sphinx recognizes :external+sphinx:ref:`some
info fields<info-field-lists>`, such as ``param`` and ``return``, and formats
them nicely.

.. code-block:: c

  /**
   * The baznicator.
   *
   * :param foo: The Foo parameter.
   * :param bar: The Bar parameter.
   * :return: 0 on success, non-zero error code on error.
   * :since: v0.1
   */
  int baz(int foo, int bar);

.. _field lists: https://docutils.sourceforge.io/docs/ref/rst/restructuredtext.html#field-lists

.. _extending-the-syntax:

Extending the Syntax
--------------------

Hawkmoth supports :ref:`extending <extending>` the syntax using :ref:`built-in
<built-in-extensions>` and custom extensions that convert the comments to
reStructuredText.

The :ref:`hawkmoth.ext.javadoc` extension provides limited support for Javadoc_
and Doxygen_ style comments, and the :ref:`hawkmoth.ext.napoleon` extension
provides support for :external+sphinx:py:mod:`sphinx.ext.napoleon` style
comments.

.. _Javadoc: https://www.oracle.com/java/technologies/javase/javadoc.html

.. _Doxygen: https://www.doxygen.nl/

.. _cross-referencing:

Cross-Referencing C and C++ Constructs
--------------------------------------

Under the hood, the :ref:`Hawkmoth directives <directives>` generate
corresponding :external+sphinx:doc:`C <usage/domains/c>` and
:external+sphinx:doc:`C++ <usage/domains/cpp>` domain directives. For example,
:rst:dir:`c:autovar` produces :external+sphinx:rst:dir:`c:var`. Use the Sphinx
:external+sphinx:ref:`C Domain Roles <c-xref-roles>` and
:external+sphinx:ref:`C++ Domain Roles<cpp-xref-roles>` for cross-referencing
accordingly.

For example:

- ``:c:var:`name``` for variables.

- ``:c:func:`name``` for functions and function-like macros.

- ``:cpp:class:`name``` for classes.

- ``:c:member:`name.membername``` for struct and union members.

The C++ Domain does not have a ``cpp:macro`` directive, however, so all macros
generate documentation using the C Domain :external+sphinx:rst:dir:`c:macro`
directive. This also means macros have to be referenced using the
:external+sphinx:rst:role:`c:macro` role, even when otherwise using C++ Domain
directives.

See the Sphinx :external+sphinx:ref:`basic-domain-markup` and generic
:external+sphinx:ref:`xref-syntax` for further details on cross-referencing, and
how to specify the default domain for brevity.
