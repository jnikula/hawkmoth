
|badge-tag| |badge-license| |badge-rtd| |badge-pypi|

.. |badge-tag| image:: https://img.shields.io/github/v/tag/jnikula/hawkmoth
		       :target: https://github.com/jnikula/hawkmoth/blob/master/CHANGELOG.rst
		       :alt: GitHub tag (latest SemVer)

.. |badge-license| image:: https://img.shields.io/github/license/jnikula/hawkmoth
			   :target: https://opensource.org/licenses/BSD-2-Clause
			   :alt: BSD-2-Clause

.. |badge-rtd| image:: https://img.shields.io/readthedocs/hawkmoth
		       :target: https://hawkmoth.readthedocs.io/en/latest/
		       :alt: Read the Docs

.. |badge-pypi| image:: https://img.shields.io/pypi/dm/hawkmoth
			:target: https://pypi.org/project/hawkmoth/
			:alt: PyPI Downloads

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

Documentation on how to install and configure Hawkmoth, and write documentation
comments, with examples, is available in the ``doc`` directory in the source
tree, obviously in Sphinx format and using the directive extension. Pre-built
documentation `showcasing what Hawkmoth can do`_ is available at `Read the
Docs`_.

.. _showcasing what Hawkmoth can do: https://hawkmoth.readthedocs.io/en/latest/examples.html

.. _Read the Docs: https://hawkmoth.readthedocs.io/

Installation
------------

You can install Hawkmoth from PyPI_ with::

  pip install hawkmoth

You'll additionally need to install Clang and Python 3 bindings for it through
your distro's package manager; they are not available via PyPI. For further
details, see the documentation.

Alternatively, installation packages are available for:

* `Arch Linux`_

There are also Docker images `jnikula/hawkmoth`_ and
`jnikula/hawkmoth-latexpdf`_ at Docker Hub.

In Sphinx ``conf.py``, add ``hawkmoth`` to ``extensions``, and point
``cautodoc_root`` at the source tree. See the extension documentation for
details.

.. _PyPI: https://pypi.org/project/hawkmoth/

.. _Arch Linux: https://aur.archlinux.org/packages/?K=hawkmoth

.. _jnikula/hawkmoth-latexpdf: https://hub.docker.com/repository/docker/jnikula/hawkmoth-latexpdf

.. _jnikula/hawkmoth: https://hub.docker.com/repository/docker/jnikula/hawkmoth

Development and Contributing
----------------------------

Hawkmoth source code is available on GitHub_. The development version can be
checked out via ``git`` using this command::

  git clone https://github.com/jnikula/hawkmoth.git

Please file bugs and feature requests as GitHub issues. Contributions are
welcome both as GitHub pull requests (preferred) and as emailed patches to the
mailing list.

See `CONTRIBUTING.rst`_ for more details.

.. _GitHub: https://github.com/jnikula/hawkmoth

.. _CONTRIBUTING.rst: https://github.com/jnikula/hawkmoth/blob/master/CONTRIBUTING.rst

Dependencies
------------

Dependencies and their minimum versions:

- Python 3.6
- Sphinx 3
- Clang library 6
- Python 3 Bindings for Clang library 6

There are additional development and testing dependencies recorded in
`setup.cfg`_.

.. _setup.cfg: https://github.com/jnikula/hawkmoth/blob/master/setup.cfg

License
-------

Hawkmoth is free software, released under the `2-Clause BSD License`_.

.. _2-Clause BSD License: https://opensource.org/licenses/BSD-2-Clause

Contact
-------

IRC channel ``#hawkmoth`` on `OFTC IRC network`_.

Mailing list hawkmoth@freelists.org. Subscription information at the `list home
page`_.

.. _OFTC IRC network: https://www.oftc.net/

.. _list home page: https://www.freelists.org/list/hawkmoth
