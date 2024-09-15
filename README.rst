
|badge-tag| |badge-license| |badge-ci| |badge-docs| |badge-rtd| |badge-pypi|

.. |badge-tag| image:: https://img.shields.io/github/v/tag/jnikula/hawkmoth
		       :target: https://github.com/jnikula/hawkmoth/blob/master/CHANGELOG.rst
		       :alt: GitHub tag (latest SemVer)

.. |badge-license| image:: https://img.shields.io/github/license/jnikula/hawkmoth
			   :target: https://opensource.org/licenses/BSD-2-Clause
			   :alt: BSD-2-Clause

.. |badge-ci| image:: https://github.com/jnikula/hawkmoth/actions/workflows/makefile.yml/badge.svg
		      :target: https://github.com/jnikula/hawkmoth/actions/workflows/makefile.yml
		      :alt: Makefile CI

.. |badge-docs| image:: https://github.com/jnikula/hawkmoth/actions/workflows/docs.yml/badge.svg
			:target: https://github.com/jnikula/hawkmoth/actions/workflows/docs.yml
			:alt: Build and Deploy Documentation

.. |badge-rtd| image:: https://img.shields.io/readthedocs/hawkmoth
		       :target: https://hawkmoth.readthedocs.io/en/latest/
		       :alt: Read the Docs

.. |badge-pypi| image:: https://img.shields.io/pypi/dm/hawkmoth
			:target: https://pypi.org/project/hawkmoth/
			:alt: PyPI Downloads

Hawkmoth - Sphinx Autodoc for C
===============================

Hawkmoth is a minimalistic Sphinx_ `C and C++ Domain`_ autodoc directive
extension to incorporate formatted C and C++ source code comments written in
reStructuredText_ into Sphinx based documentation. It uses Clang Python Bindings
for parsing, and generates C and C++ Domain directives for C and C++ API
documentation, and more. In short, Hawkmoth is Sphinx Autodoc for C/C++.

Hawkmoth aims to be a compelling alternative for documenting C and C++ projects
using Sphinx, mainly through its simplicity of design, implementation and use.

.. _Sphinx: http://www.sphinx-doc.org

.. _C and C++ Domain: http://www.sphinx-doc.org/en/stable/domains.html

.. _reStructuredText: http://docutils.sourceforge.net/rst.html

Example
-------

Given C source code with rather familiar looking documentation comments::

  /**
   * Get foo out of bar.
   *
   * :param bar: Name of the bar.
   */
  void foobar(const char *bar);

and a directive in the Sphinx project::

  .. c:autofunction:: foobar
     :file: filename.c

you can incorporate code documentation into Sphinx. It's as simple as that.

You can document functions, their parameters and return values, structs,
classes, unions, their members, macros, function-like macros, enums, enumeration
constants, typedefs, variables, as well as have generic documentation comments
not attached to any symbols.

See the documentation `examples`_ section for more, with sample output.

.. _examples: https://jnikula.github.io/hawkmoth/stable/examples.html

Documentation
-------------

Documentation on how to install, configure and use Hawkmoth, as well as write
documentation comments, with examples, is available for both the `latest
release`_ and the `version currently in development`_.

The same is also hosted at `Read the Docs`_.

.. _latest release: https://jnikula.github.io/hawkmoth/stable/

.. _version currently in development: https://jnikula.github.io/hawkmoth/dev/

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

In Sphinx ``conf.py``, add ``hawkmoth`` to ``extensions``, and point
``hawkmoth_root`` at the source tree. See the extension documentation for
details.

.. _PyPI: https://pypi.org/project/hawkmoth/

.. _Arch Linux: https://aur.archlinux.org/packages/?K=hawkmoth

Development and Contributing
----------------------------

Hawkmoth source code is available on GitHub_. The development version can be
checked out via ``git`` using this command::

  git clone https://github.com/jnikula/hawkmoth.git

Please file bugs and feature requests as GitHub issues_. Contributions are
welcome as GitHub pull requests.

See the `developer documentation`_ for details.

.. _GitHub: https://github.com/jnikula/hawkmoth

.. _developer documentation: https://jnikula.github.io/hawkmoth/dev/developer/

Dependencies
------------

Dependencies and their minimum versions:

- Python 3.9
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

IRC channel ``#hawkmoth`` on `OFTC IRC network`_. GitHub issues_ and
discussions_.

.. _OFTC IRC network: https://www.oftc.net/

.. _issues: https://github.com/jnikula/hawkmoth/issues

.. _discussions: https://github.com/jnikula/hawkmoth/discussions
