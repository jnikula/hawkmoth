.. _extension:

C Autodoc Extension
===================

Hawkmoth provides a Sphinx extension that adds new directives to the Sphinx
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
   take a (multi-line) comment string as a parameter, and return the transformed
   string. This can be used to perform custom conversions of the comments,
   including, but not limited to, Javadoc-style compat conversions.

   The special key ``None``, if present, is used to convert everything, unless
   overridden in the directive ``transform`` option. The special value ``None``
   means no transformation is to be done.

   For example, this configuration would transform everything using
   ``default_transform`` function by default, unless overridden in the directive
   ``transform`` option with ``javadoc`` or ``none``. The former would use
   ``javadoc_transform`` function, and the latter would bypass transform
   altogether.

   .. code-block:: python

      cautodoc_transformations = {
          None: default_transform,
	  'javadoc': javadoc_transform,
	  'none': None,
      }

   The example below shows how to use Hawkmoth's existing compat functions in
   ``conf.py``, for migration from deprecated ``cautodoc_compat``. Also replace
   ``:compat:`` with ``:transform:``.

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
   :type: list

   A list of arguments to pass to ``clang`` while parsing the source, typically
   to add directories to include file search path, or to define macros for
   conditional compilation. No arguments are passed by default.

   Example:

   .. code-block:: python

      cautodoc_clang = ['-I/path/to/include', '-DHAWKMOTH']

   Hawkmoth provides a convenience helper for querying the include path from the
   compiler, and providing them as ``-I`` options:

   .. code-block:: python

      from hawkmoth.util import compiler

      cautodoc_clang = compiler.get_include_args()

   You can also pass in the compiler to use, for example
   ``get_include_args('gcc')``.

Directives
----------

Hawkmoth provides several new directives for incorporating documentation
comments from C sources into the reStructuredText document. The
:rst:dir:`c:autodoc` directive simply includes all the comments from any number
of files, while the rest are for including documentation for specific symbols.

.. rst:directive:: .. c:autodoc:: filename-pattern [...]

   Incorporate documentation comments from the files specified by the space
   separated list of filename patterns given as arguments. The patterns are
   interpreted relative to the :data:`cautodoc_root` configuration option.

   .. rst:directive:option:: transform
      :type: text

      Name of the transformation function specified in
      :data:`cautodoc_transformations` to use for converting the comments. This
      value overrides the default in :data:`cautodoc_transformations`.

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

      The ``clang`` option extends the :data:`cautodoc_clang` configuration
      option.

.. rst:directive:: .. c:autovar:: name

   .. rst:directive:option:: file
      :type: text

      The ``file`` option specifies to file to parse. The filename is
      interpreted relative to the :data:`cautodoc_root` configuration
      option. (For the time being, this option is mandatory.)

   Incorporate the documentation comment for the variable ``name`` in the file
   ``file``.

.. rst:directive:: .. c:autotype:: name

   Same as :rst:dir:`c:autovar` but for typedefs.

.. rst:directive:: .. c:automacro:: name

   Same as :rst:dir:`c:autovar` but for macros, including function-like macros.

.. rst:directive:: .. c:autofunction:: name

   Same as :rst:dir:`c:autovar` but for functions. (Use :rst:dir:`c:automacro`
   for function-like macros.)

.. rst:directive:: .. c:autostruct:: name

   .. rst:directive:option:: members
      :type: text

      The ``members`` option specifies the struct members to include. If
      ``members`` is not specified, do not include member documentation. If
      ``members`` is specified without arguments, include all member
      documentation recursively. If ``members`` is specified with a
      comma-separated list of arguments, include all specified member
      documentation recursively.

   Same as :rst:dir:`c:autovar` but for structs. Additionally, filter by
   ``members``.

.. rst:directive:: .. c:autounion:: name

   Same as :rst:dir:`c:autostruct` but for unions.

.. rst:directive:: .. c:autoenum:: name

   Same as :rst:dir:`c:autostruct` but for enums. The enumeration constants are
   considered ``members`` and are filtered accordingly.


Examples
--------

The basic usage is:

.. code-block:: rst

   .. c:autodoc:: interface.h

Individual symbols:

.. code-block:: rst

   .. c:autofunction:: foo
      :file: interface.h

   .. c:autostruct:: bar
      :file: interface.h

Several files with compatibility and compiler options:

.. code-block:: rst

   .. c:autodoc:: api/*.[ch] interface.h
      :compat: javadoc-basic
      :clang: -DHAWKMOTH
