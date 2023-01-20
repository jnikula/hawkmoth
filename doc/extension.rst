.. _extension:

C Autodoc Extension
===================

Hawkmoth provides a Sphinx extension that adds :ref:`new directives
<directives>` to the Sphinx :any:`C domain <sphinx:c-domain>` to incorporate
formatted C source code comments into a document. Hawkmoth is Sphinx
:any:`sphinx:sphinx.ext.autodoc` for C.

For this to work, the documentation comments must of course be written in
correct reStructuredText. See :ref:`documentation comment syntax <syntax>` for
details.

See :ref:`installation` on how to install the Hawkmoth package and its
dependencies.

Usage
-----

Add ``hawkmoth`` to :confval:`sphinx:extensions` in ``conf.py``. Note that
depending on the packaging and installation directory, this may require
adjusting the :envvar:`python:PYTHONPATH`.

For example:

.. code-block:: python

   extensions.append('hawkmoth')

Configuration
-------------

The extension has a few configuration options that can be set in ``conf.py``:

.. py:data:: hawkmoth_root
   :type: str

   Path to the root of the source files. Defaults to the
   :term:`sphinx:configuration directory`, i.e. the directory containing
   ``conf.py``.

   To use paths relative to the configuration directory, use
   :func:`python:os.path.abspath`, for example:

   .. code-block:: python

      import os
      hawkmoth_root = os.path.abspath('my/sources/dir')

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
   ``conf.py``.

   .. code-block:: python

      from hawkmoth.util import doccompat
      cautodoc_transformations = {
          'javadoc-basic': doccompat.javadoc,
          'javadoc-liberal': doccompat.javadoc_liberal,
          'kernel-doc': doccompat.kerneldoc,
      }

.. py:data:: hawkmoth_clang
   :type: list

   A list of arguments to pass to ``clang`` while parsing the source, typically
   to add directories to include file search path, or to define macros for
   conditional compilation. No arguments are passed by default.

   Example:

   .. code-block:: python

      hawkmoth_clang = ['-I/path/to/include', '-DHAWKMOTH']

   Hawkmoth provides a convenience helper for querying the include path from the
   compiler, and providing them as ``-I`` options:

   .. code-block:: python

      from hawkmoth.util import compiler

      hawkmoth_clang = compiler.get_include_args()

   You can also pass in the compiler to use, for example
   ``get_include_args('gcc')``.

.. py:data:: cautodoc_root
   :type: str

   Equivalent to :py:data:`hawkmoth_root`.

   .. warning::

      The ``cautodoc_root`` option has been deprecated in favour of the
      :py:data:`hawkmoth_root` option and will be removed in the future.

.. py:data:: cautodoc_clang
   :type: str

   Equivalent to :py:data:`hawkmoth_clang`.

   .. warning::

      The ``cautodoc_clang`` option has been deprecated in favour of
      the :py:data:`hawkmoth_clang` option and will be removed in the
      future.
