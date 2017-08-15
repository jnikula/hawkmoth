Syntax
======

Documentation comments are C language block comments that begin with "/\*\*".

For multi-line comments it's recommended to place the opening delimeter "/\*\*"
and closing delimeter "\*/" on lines of their own, and prefix the lines in
between with " \* ". Because reStructuredText is fussy about indentation, it's
recommended to indent the actual documentation at the third column::

  /**
   * The quick brown fox jumps
   * over the lazy dog.
   */

One-liners are okay too::

  /** The quick brown fox jumps over the lazy dog. */

All documentation comments preceding C constructs are attached to them, and
result in C Domain directives being added for them. This includes struct and
union members and enumerations.

Documentation comments followed by comments (documentation or not) are included
as generic documentation.

Tags
----

Use reStructuredText field lists for documenting function parameters, return
values, and arbitrary other data::

  /**
   * The baznicator.
   *
   * :param foo: The Foo parameter.
   * :param bar: The Bar parameter.
   * :return: 0 on success, non-zero error code on error.
   * :since: v0.1
   */
  int baz(int foo, int bar);

For compatibility with Javadoc and Doxygen, Hawkmoth supports @param and
@return. Arbitrary @tag is converted to :tag:::

  /**
   * The baznicator.
   *
   * @param foo The Foo parameter.
   * @param bar The Bar parameter.
   * @return 0 on success, non-zero error code on error.
   * @since v0.1
   */
  int baz(int foo, int bar);
