C Autodoc Extension
===================

Hawkmoth provides ``hawkmoth.cautodoc`` Sphinx extension that adds a new
``c:autodoc`` directive to the Sphinx `C Domain`_ to incorporate formatted C
source code comments into a document. This could be thought of as a version of
`Python autodoc`_ for C.

For this to work, the documentation comments must of course be written in
correct reStructuredText. See syntax for details.

.. _C Domain: http://www.sphinx-doc.org/en/stable/domains.html#the-c-domain

.. _Python autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html

Installation
------------

Add ``hawkmoth.cautodoc`` to ``extensions`` in ``conf.py``.

Configuration
-------------

The ``hawkmoth.cautodoc`` extension has a few configuration options that can be
set in ``conf.py``.

``cautodoc_root``
~~~~~~~~~~~~~~~~~

Path to the root of the source files. Defaults to ``.``.

``cautodoc_compat``
~~~~~~~~~~~~~~~~~~~

Compatibility option. One of ``none`` (the default), ``javadoc-basic``,
``javadoc-liberal``, and ``kernel-doc``. This can be used to perform a limited
conversion of Javadoc-style tags to reStructuredText.

.. warning:: The compatibility options are likely to change.

``cautodoc_clang``
~~~~~~~~~~~~~~~~~~

A comma separated list of arguments to pass to ``clang`` while parsing the
source, typically to define macros for conditional compilation, for example
``-DHAWKMOTH``. No additional arguments are passed by default.

Directive
---------

The single directive provided by ``hawkmoth.cautodoc`` is very simple.

.. rst:directive:: .. c:autodoc:: filename-pattern [...]

   Incorporate documentation comments from the files specified by the space
   separated list of filename patterns given as arguments. The patterns are
   interpreted relative to the ``cautodoc_root`` configuration option.

   The ``compat`` option overrides the ``cautodoc_compat`` configuration option.

   The ``clang`` option overrides the ``cautodoc_clang`` configuration option.

Examples
--------

The basic usage is:

.. code-block:: rst

  .. c:autodoc:: interface.h

Several files with compatibility and compiler options:

.. code-block:: rst

  .. c:autodoc:: api/*.[ch] interface.h
     :compat: javadoc-basic
     :clang: -DHAWKMOTH
