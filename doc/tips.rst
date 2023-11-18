.. _tips:

Tips and Tricks
===============

Here is a small collection of tips and tricks on how to use Sphinx and Hawkmoth
for documenting C and C++ code.

Function Parameter Direction
----------------------------

Sphinx does not have a dedicated way of expressing the parameter direction
similar to Doxygen `@param[dir]`_ command. One approach to emulate this is to
define reStructuredText `replacement texts`_, and use them.

For example:

.. code-block:: python
   :caption: conf.py

   rst_prolog = '''
   .. |in| replace:: **[in]**
   .. |out| replace:: **[out]**
   .. |in,out| replace:: **[in,out]**
   '''

.. code-block:: c
   :caption: source code

   /**
    * :param foo: |in| Foo parameter.
    */
   void bar(char *foo);

By using replacement text, the direction stands out in the source code, you get
warnings for typos, and you can modify the appearance across documentation in
one place. Instead of ``**[in]**``, you might use ``⇒``, or whatever you prefer.

.. _@param[dir]: https://www.doxygen.nl/manual/commands.html#cmdparam

.. _replacement texts: https://docutils.sourceforge.io/docs/ref/rst/directives.html#replacement-text

Including Source Code Blocks
----------------------------

Doxygen has the `@include`_ and `@snippet`_ commands to include a source file or
a fragment of one into documentation as a block of code.

The Sphinx alternative is :external+sphinx:rst:dir:`literalinclude`. The
``:start-after:`` and ``:end-before:`` options can be used to mimic the
``block_id`` of ``@snippet``, but there's plenty more.

.. code-block:: rst

   .. literalinclude:: path/to/source.c
      :start-after: Adding a resource
      :end-before: Adding a resource

.. _@include: https://www.doxygen.nl/manual/commands.html#cmdinclude

.. _@snippet: https://www.doxygen.nl/manual/commands.html#cmdsnippet
