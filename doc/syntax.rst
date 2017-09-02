.. _syntax:

Syntax
======

For the ``c:autodoc`` directive to work, the C source code must be documented
using specific documentation comment style, and the comments must follow
reStructuredText markup.

Optionally, there's limited support for some Javadoc_ and Doxygen_ style
constructs for compatibility.

Documentation Comments
----------------------

Documentation comments are C language block comments that begin with "/\*\*".

Because reStructuredText is sensitive about indentation, it's strongly
recommended, even if not strictly required, to follow a uniform style for
multi-line comments. Place the opening delimeter "/\*\*" and closing delimeter
"\*/" on lines of their own, and prefix the lines in between with " \* ". Indent
the actual documentation at the third column, to let Hawkmoth consistently
remove the enclosing comment markers:

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

Compatibility
-------------

Hawkmoth supports limited Javadoc_ and Doxygen_ style constructs for
compatibility. See the :ref:`extension documentation <extension>` on how to
enable the support.

.. code-block:: c

  /**
   * The baznicator.
   *
   * @param foo The Foo parameter.
   * @param bar The Bar parameter.
   * @return 0 on success, non-zero error code on error.
   * @since v0.1
   */
  int baz(int foo, int bar);

.. warning:: The compatibility support and its documentation are a
             work-in-progress.

.. _Javadoc: http://www.oracle.com/technetwork/java/javase/documentation/javadoc-137458.html

.. _Doxygen: http://doxygen.org/

Cross-Referencing C Constructs
------------------------------

Use the C Domain roles for `cross-referencing C constructs`_ as follows:

- ``:c:data:`name``` for variables.

- ``:c:func:`name``` for functions and function-like macros.

- ``:c:macro:`name``` for simple macros and enumeration constants.

- ``:c:type:`name``` for structs, unions, enums, and typedefs.

- ``:c:member:`name.membername``` for struct and union members.

See the Sphinx `domain documentation`_ and generic `cross-referencing syntax`_
for further details on cross-referencing, and how to specify the default domain
for brevity.

.. _domain documentation: http://www.sphinx-doc.org/en/stable/domains.html

.. _cross-referencing C constructs: http://www.sphinx-doc.org/en/stable/domains.html#cross-referencing-c-constructs

.. _cross-referencing syntax: http://www.sphinx-doc.org/en/stable/markup/inline.html#xref-syntax
