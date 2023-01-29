.. _syntax:

Syntax
======

For the :ref:`Hawkmoth autodoc directives <directives>` to work, the C source
code must be documented using specific documentation comment style, and the
comments must follow reStructuredText markup.

Optionally, the syntax may be :ref:`extended <extending-the-syntax>` to support
e.g. Javadoc and Napoleon style comments.

See :ref:`the examples section <examples>` for a quick tour of what's possible,
and read on for documentation comment formatting details.

Documentation Comments
----------------------

Documentation comments are C language block comments that begin with ``/**``.

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

All documentation comments preceding C constructs are attached to them, and
result in C Domain directives being added for them. This includes macros,
functions, struct and union members, enumerations, etc.

Documentation comments followed by comments (documentation or not) are included
as generic documentation.

Tags
----

Use reStructuredText `field lists`_ for documenting function parameters, return
values, and arbitrary other data:

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

.. _field lists: http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists

.. _extending-the-syntax:

Extending the Syntax
--------------------

Hawkmoth supports :ref:`extending <extending>` the syntax using :ref:`built-in
<built-in-extensions>` and custom extensions that convert the comments to
reStructuredText.

The :ref:`hawkmoth.ext.javadoc` extension provides limited support for Javadoc_
style comments, and the :ref:`hawkmoth.ext.napoleon` extension provides support
for :external+sphinx:py:mod:`sphinx.ext.napoleon` style comments.

.. _Javadoc: https://www.oracle.com/technetwork/java/javase/documentation/javadoc-137458.html

Cross-Referencing C Constructs
------------------------------

Use :external+sphinx:ref:`c-domain` roles for cross-referencing as follows:

- ``:c:data:`name``` for variables.

- ``:c:func:`name``` for functions and function-like macros.

- ``:c:macro:`name``` for simple macros and enumeration constants.

- ``:c:type:`name``` for structs, unions, enums, and typedefs.

- ``:c:member:`name.membername``` for struct and union members.

See the Sphinx :external+sphinx:ref:`basic-domain-markup` and generic
:external+sphinx:ref:`xref-syntax` for further details on cross-referencing, and
how to specify the default domain for brevity.
