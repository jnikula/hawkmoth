.. _extension:

C Autodoc Extension
===================

Hawkmoth provides a Sphinx extension that adds a new directive to the Sphinx
:any:`C domain <sphinx:c-domain>` to incorporate formatted C source code
comments into a document. Hawkmoth is Sphinx :any:`sphinx:sphinx.ext.autodoc`
for C.

For this to work, the documentation comments must of course be written in
correct reStructuredText. See :ref:`documentation comment syntax <syntax>` for
details.

See :ref:`installation` on how to install the Hawkmoth package and its
dependencies.

Usage
-----

Add ``hawkmoth`` to :data:`sphinx:extensions` in ``conf.py``. Note that
depending on the packaging and installation directory, this may require
adjusting the :envvar:`python:PYTHONPATH`.

For example:

.. code-block:: python

   extensions.append('hawkmoth')

Configuration
-------------

The extension has a few configuration options that can be set in ``conf.py``:

.. py:data:: cautodoc_root
   :type: str

   Path to the root of the source files. Defaults to the
   :term:`sphinx:configuration directory`, i.e. the directory containing
   ``conf.py``.

   To use paths relative to the configuration directory, use
   :func:`python:os.path.abspath`, for example:

   .. code-block:: python

      import os
      cautodoc_root = os.path.abspath('my/sources/dir')

.. py:data:: cautodoc_transformations
   :type: dict

   Transformation functions for the :rst:dir:`c:autodoc` directive ``transform``
   option. This is a dictionary that maps names to functions. The names can be
   used in the directive ``transform`` option. The functions are expected to
   take a (multi-line) comment string and options as parameters, and return the
   transformed string. This can be used to perform custom conversions of the
   comments, including, but not limited to, Javadoc-style compat conversions.

   The special name ``default``, if present, is used to convert everything,
   unless overridden in the directive ``transform`` option. The special name
   ``none`` can be used in the ``transform`` option to bypass the default.

   This is an example of a no-op transformation:

   .. code-block:: python

      def noop(comment, **options):
          return comment

   The example below shows how to use Hawkmoth's existing compat functions in
   ``conf.py``.

   .. code-block:: python

      from hawkmoth.util import doccompat
      cautodoc_transformations = {
          'javadoc-basic': doccompat.javadoc,
          'javadoc-liberal': doccompat.javadoc_liberal,
          'kernel-doc': doccompat.kerneldoc,
      }

.. py:data:: cautodoc_compat
   :type: str

   Compatibility option. One of ``none`` (default), ``javadoc-basic``,
   ``javadoc-liberal``, and ``kernel-doc``. This can be used to perform a
   limited conversion of Javadoc-style tags to reStructuredText.

   .. warning::

      The cautodoc_compat option has been deprecated in favour of the
      :data:`cautodoc_transformations` option and the :rst:dir:`c:autodoc`
      directive ``transform`` option, and will be removed in the future.

.. py:data:: cautodoc_clang
   :type: str

   A comma separated list of arguments to pass to ``clang`` while parsing the
   source, typically to define macros for conditional compilation, for example
   ``-DHAWKMOTH``. No arguments are passed by default.

Directive
---------

This module provides the following new directive:

.. rst:directive:: .. c:autodoc:: filename-pattern [...]

   Incorporate documentation comments from the files specified by the space
   separated list of filename patterns given as arguments. The patterns are
   interpreted relative to the :data:`cautodoc_root` configuration option.

   .. rst:directive:option:: transform
      :type: text

      Name of the transformation function specified in
      :data:`cautodoc_transformations` to use for converting the comments.

      If set to ``none``, the default is overriden.

   .. rst:directive:option:: compat
      :type: text

      The ``compat`` option overrides the :data:`cautodoc_compat` configuration
      option.

      .. warning::

	 The compat option has been deprecated in favour of the
	 :data:`cautodoc_transformations` option and the :rst:dir:`c:autodoc`
	 directive ``transform`` option, and will be removed in the future.

   .. rst:directive:option:: clang
      :type: text

      The ``clang`` option overrides the :data:`cautodoc_clang` configuration
      option.

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
