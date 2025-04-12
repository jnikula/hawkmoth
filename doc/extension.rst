.. SPDX-FileCopyrightText: 2017 Jani Nikula <jani@nikula.org>
.. SPDX-FileCopyrightText: 2018 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
.. SPDX-License-Identifier: BSD-2-Clause

.. _extension:

Autodoc Extension
=================

Hawkmoth provides a Sphinx extension that adds :ref:`new directives
<directives>` to the Sphinx :external+sphinx:doc:`C <usage/domains/c>` and
:external+sphinx:doc:`C++ <usage/domains/cpp>` domains to incorporate formatted
C and C++ source code comments into a document. Hawkmoth is Sphinx
:py:mod:`sphinx.ext.autodoc` for C/C++.

For this to work, the documentation comments must of course be written in
correct reStructuredText. See :ref:`documentation comment syntax <syntax>` for
details.

Hawkmoth itself is :ref:`extensible <extending>`, and ships with some
:ref:`built-in extensions <built-in-extensions>`.

Usage
-----

Add ``hawkmoth`` to :external+sphinx:confval:`extensions` in ``conf.py``. Note
that depending on the packaging and installation directory, this may require
adjusting the :envvar:`python:PYTHONPATH`.

For example:

.. code-block:: python

   extensions.append('hawkmoth')

Configuration
-------------

The extension has a few configuration options that can be set in ``conf.py``.

See also additional configuration options in the :ref:`built-in extensions
<built-in-extensions>`.

.. py:data:: hawkmoth_root
   :type: str

   Path to the root of the source files. Defaults to the
   :external+sphinx:term:`configuration directory`, i.e. the directory
   containing ``conf.py``.

   To use paths relative to the configuration directory, use
   :func:`python:os.path.abspath`, for example:

   .. code-block:: python

      import os
      hawkmoth_root = os.path.abspath('my/sources/dir')

.. py:data:: hawkmoth_transform_default
   :type: str|None

   The default transform parameter to be passed to the
   :event:`hawkmoth-process-docstring` event. It can be overridden with the
   ``transform`` option of the :ref:`directives <directives>`. Defaults to
   ``None``.

.. py:data:: hawkmoth_compiler
   :type: str|None

   The (path to the) default compiler used by the project. This is used to
   determine the exact options needed to parse the code files by libclang
   provided the relevant options are enabled in :data:`hawkmoth_autoconf`.

   Notably, it allows hawkmoth to override libclang's default search path for
   system headers with those of the specified compiler.

   This presumes the compiler supports being called as
   ``<compiler> -x <c|c++> -E -Wp,-v /dev/null``.

   Defaults to ``clang``, which may differ from libclang's own default includes.

.. py:data:: hawkmoth_autoconf
   :type: list[str]|None

   List of options that control the automatic configuration features of
   hawkmoth. Currently supported options:

   * ``'stdinc'``: override the standard include paths of libclang with those of
     the specified compiler (see :data:`hawkmoth_compiler`).

     This is a shortcut to specify ``-nostdinc -I<dir 1> ... -I<dir n>`` in
     :data:`hawkmoth_clang` with the search directories of the specified
     compiler.

   Defaults to ``['stdinc']``. Set to ``None`` (or ``[]``) to disable automatic
   configuration, falling back to libclang's defaults.

.. py:data:: hawkmoth_clang
   :type: list[str]

   A list of arguments to pass to ``clang`` while parsing the source, typically
   to add directories to include file search path, or to define macros for
   conditional compilation. No arguments are passed by default.

   Example:

   .. code-block:: python

      hawkmoth_clang = ['-I/path/to/include', '-DHAWKMOTH']

.. py:data:: hawkmoth_clang_c
   :type: list[str]

   Arguments to pass to ``clang`` after :data:`hawkmoth_clang` in the C domain
   only.

.. py:data:: hawkmoth_clang_cpp
   :type: list[str]

   Arguments to pass to ``clang`` after :data:`hawkmoth_clang` in the C++ domain
   only.

.. py:data:: hawkmoth_source_uri
   :type: str|None

   A template URI to source code. If set, add links to externally hosted source
   code for each documented symbol, similar to the :external+sphinx:doc:`Sphinx
   linkcode extension <usage/extensions/linkcode>`. Defaults to ``None``.

   The template URI will be formatted using
   :external+python:py:meth:`str.format`, with the following replacement fields:

   ``{source}``
     Path to source file relative to :py:data:`hawkmoth_root`.
   ``{line}``
     Line number in source file.

   Example:

   .. code-block:: python

      hawkmoth_source_uri = 'https://example.org/src/{source}#L{line}'
