Hawkmoth
========

Hawkmoth is a minimalistic Sphinx_ `C Domain`_ autodoc directive extension to
incorporate formatted C source code comments into Sphinx based documentation. It
generates C Domain directives automatically for C API documentation, but is not
limited to that.

.. _Sphinx: http://www.sphinx-doc.org

.. _C Domain: http://www.sphinx-doc.org/en/stable/domains.html

Larval Stage
------------

Hawkmoth is a project very much in its infancy. The main goal is pretty clear:
Use Clang Python Bindings to extract reStructuredText_ documentation comments
from source into Sphinx, and keep it simple. The rough concept is there and
functional, but there are bugs, documentation is lacking, testing is inadequate,
there are no promises about backwards compatible changes, it's not packaged,
etc.

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

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

reStructuredText style field lists are the native way of documenting parameters
and return values and so on, but there's limited compatibility with Javadoc_ or
Doxygen_ style ``@tags``.

.. _Javadoc: http://www.oracle.com/technetwork/java/javase/documentation/index-jsp-135444.html

.. _Doxygen: http://www.stack.nl/~dimitri/doxygen/

Dependencies
------------

 * python-clang-3.8
 * libclang-3.8-dev
 * libclang1-3.8
 * Sphinx 1.3

Installation
------------

In Sphinx ``conf.py``, point ``sys.path`` at Hawkmoth, add ``cautodoc`` to
``extensions``, and point ``cautodoc_root`` at the source tree.

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
