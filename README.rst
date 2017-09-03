Hawkmoth
========

Hawkmoth is a minimalistic Sphinx_ `C Domain`_ autodoc directive extension to
incorporate formatted C source code comments written in reStructuredText_ into
Sphinx based documentation. It uses Clang Python Bindings for parsing, and
generates C Domain directives for C API documentation, and more. In short,
Hawkmoth is Sphinx Autodoc for C.

Hawkmoth aims to be a compelling alternative for documenting C projects using
Sphinx, mainly through its simplicity of design, implementation and use.

.. _Sphinx: http://www.sphinx-doc.org

.. _C Domain: http://www.sphinx-doc.org/en/stable/domains.html

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

Larval Stage
------------

Hawkmoth is a project very much in its infancy. The main idea is clear, the
rough implementation is there and mostly working, even documentation is starting
to shape up, but there are bugs, testing is inadequate, there are no promises
about backwards compatible changes, it's not packaged, etc. But it's usable if
you're not afraid to try software that might be a bit rough around the edges.

Example
-------

Given C source code with rather familiar looking documentation comments::

  /**
   * Get foo out of bar.
   */
  void foobar();

and a directive in the Sphinx project::

  .. c:autodoc:: filename.c

you can incorporate code documentation into Sphinx. It's as simple as that.

You can document functions, parameters, return values, structs, unions, their
members, macros, function-like macros, enums, enumerations, typedefs, variables,
as well as have generic documentation comments not attached to any symbols.

reStructuredText style field lists are the native way of documenting function
parameters and return values and so on, but there's limited compatibility with
Javadoc_ or Doxygen_ style ``@tags``.

.. _Javadoc: http://www.oracle.com/technetwork/java/javase/documentation/index-jsp-135444.html

.. _Doxygen: http://www.stack.nl/~dimitri/doxygen/

Documentation
-------------

More documentation, with examples, is available in the ``doc`` directory in the
source tree, obviously in Sphinx format and using the directive
extension. Pre-built documentation is available at `Read the Docs`_.

.. _Read the Docs: https://hawkmoth.readthedocs.io/

Download
--------

Hawkmoth source code is available on GitHub_. The development version can be
checked out via ``git`` using this command::

  git clone https://github.com/jnikula/hawkmoth.git

.. _GitHub: https://github.com/jnikula/hawkmoth


Dependencies
------------

- Sphinx 1.3
- python-clang-3.8
- libclang-3.8-dev
- libclang1-3.8

Hawkmoth should be compatible with both Python 2 and 3, but due to lack of
packaging of Clang Python Bindings for Python 3, it's currently being developed
and tested on Python 2 only.

Installation
------------

In Sphinx ``conf.py``, point ``sys.path`` at Hawkmoth, add ``hawkmoth.cautodoc``
to ``extensions``, and point ``cautodoc_root`` at the source tree.

(Did I say the project is in its early stages?)

License
-------

Hawkmoth is free software, released under the `2-Clause BSD License`_.

.. _2-Clause BSD License: https://opensource.org/licenses/BSD-2-Clause

Contact
-------

IRC channel ``#hawkmoth`` on freenode_.

Mailing list hawkmoth@freelists.org. Subscription information at the `list home
page`_.

.. _freenode: https://freenode.net/

.. _list home page: https://www.freelists.org/list/hawkmoth
