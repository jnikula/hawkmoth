Hawkmoth - Sphinx Autodoc for C
===============================

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

You can document functions, their parameters and return values, structs, unions,
their members, macros, function-like macros, enums, enumeration constants,
typedefs, variables, as well as have generic documentation comments not attached
to any symbols.

Documentation
-------------

Documentation on how to configure Hawkmoth and write documentation comments,
with examples, is available in the ``doc`` directory in the source tree,
obviously in Sphinx format and using the directive extension. Pre-built
documentation `showcasing what Hawkmoth can do`_ is available at `Read the
Docs`_.

.. _showcasing what Hawkmoth can do: https://hawkmoth.readthedocs.io/en/latest/examples.html

.. _Read the Docs: https://hawkmoth.readthedocs.io/

Installation
------------

You can install Hawkmoth from PyPI_ with::

  pip install hawkmoth

You'll additionally need to install Clang and Python 3 bindings for it through
your distro's package manager; they are not available via PyPI. You may also
need to set ``LD_LIBRARY_PATH`` so that the Clang library can be found. For
example::

  export LD_LIBRARY_PATH=$(llvm-config --libdir)

Alternatively, installation packages are available for:

* `Arch Linux`_

In Sphinx ``conf.py``, add ``hawkmoth`` to ``extensions``, and point
``cautodoc_root`` at the source tree. See the extension documentation for
details.

.. _PyPI: https://pypi.org/project/hawkmoth/

.. _Arch Linux: https://aur.archlinux.org/packages/?K=hawkmoth

Development and Contributing
----------------------------

Hawkmoth source code is available on GitHub_. The development version can be
checked out via ``git`` using this command::

  git clone https://github.com/jnikula/hawkmoth.git

Please file bugs and feature requests as GitHub issues. Contributions are
welcome both as emailed patches to the mailing list and as pull requests.

.. _GitHub: https://github.com/jnikula/hawkmoth

Dependencies
------------

- Python 3.4
- Sphinx 1.8
- Clang 6.0
- Python 3 Bindings for Clang 6.0
- sphinx-testing 1.0.0 (for development)

These are the versions Hawkmoth is currently being developed and tested
against. Other versions might work, but no guarantees.

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
