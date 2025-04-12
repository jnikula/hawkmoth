.. SPDX-FileCopyrightText: 2021 Jani Nikula <jani@nikula.org>
.. SPDX-FileCopyrightText: 2023 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
.. SPDX-License-Identifier: BSD-2-Clause

.. _directives:

Directives
==========

Hawkmoth provides several new directives for incorporating :ref:`documentation
comments <syntax>` from C/C++ source files into the reStructuredText document.
There are three main types of directives, for incorporating documentation from
entire files, for single objects, and for composite objects optionally with
members.

Source Files
------------

The :rst:dir:`c:autodoc` and :rst:dir:`cpp:autodoc` directives simply include
all the documentation comments from any number of files. This is the most basic
and quickest way to generate documentation, but offers no control over what gets
included.

.. rst:directive:: .. c:autodoc:: filename-pattern [...]
.. rst:directive:: .. cpp:autodoc:: filename-pattern [...]

   Incorporate documentation comments from the files specified by the space
   separated list of filename patterns given as arguments. The patterns are
   interpreted relative to the :data:`hawkmoth_root` configuration option.

   .. rst:directive:option:: transform
      :type: text

      Override :data:`hawkmoth_transform_default` for the ``transform``
      parameter value of the :event:`hawkmoth-process-docstring` event.

   .. rst:directive:option:: clang
      :type: text

      The ``clang`` option extends the :data:`hawkmoth_clang` configuration
      option.

   For example:

   .. code-block:: rst

      .. c:autodoc:: interface.h

      .. c:autodoc:: api/*.[ch] interface.h
         :clang: -DHAWKMOTH

Variables, Types, Macros, and Functions
---------------------------------------

The :rst:dir:`c:autovar`, :rst:dir:`c:autotype`, :rst:dir:`c:automacro`, and
:rst:dir:`c:autofunction` directives and their C++ domain counterparts
incorporate the documentation comment for the specified object in the specified
file.

The directives support all the same directive options as :rst:dir:`c:autodoc`
and :rst:dir:`cpp:autodoc`, adding the ``file`` option.

.. rst:directive:: .. c:autovar:: name
.. rst:directive:: .. cpp:autovar:: name

   Incorporate the documentation comment for the variable ``name``.

   If ``file`` is specified, look up ``name`` there, otherwise look up ``name``
   in all previously parsed files in the current document.

   .. rst:directive:option:: file
      :type: text

      The ``file`` option specifies the file to look up ``name`` in. This is
      required if the file has not been parsed yet, and to disambiguate if
      ``name`` is found in multiple files.

      The filename is interpreted relative to the :data:`hawkmoth_root`
      configuration option.

   For example:

   .. code-block:: rst

      .. c:autovar:: example_variable
         :file: example_file.c

      .. c:autovar:: another_variable

.. rst:directive:: .. c:autotype:: name
.. rst:directive:: .. cpp:autotype:: name

   Same as :rst:dir:`c:autovar` but for typedefs.

   .. code-block:: rst

      .. c:autotype:: example_type_t
         :file: example_file.c

.. rst:directive:: .. c:automacro:: name
.. rst:directive:: .. cpp:automacro:: name

   Same as :rst:dir:`c:autovar` but for macros, including function-like macros.

   .. note::

      The :external+sphinx:doc:`C++ Domain <usage/domains/cpp>` does not have a
      ``cpp:macro`` directive, so all macros are always in the
      :external+sphinx:doc:`C Domain <usage/domains/c>`. This affects
      cross-referencing them; see :ref:`cross-referencing` for details.

   .. code-block:: rst

      .. c:automacro:: EXAMPLE_MACRO
         :file: example_file.c

.. rst:directive:: .. c:autofunction:: name
.. rst:directive:: .. cpp:autofunction:: name

   Same as :rst:dir:`c:autovar` but for functions. (Use :rst:dir:`c:automacro`
   for function-like macros.)

   .. code-block:: rst

      .. c:autofunction:: example_function
         :file: example_file.c

Structures, Classes, Unions, and Enumerations
---------------------------------------------

The :rst:dir:`c:autostruct`, :rst:dir:`c:autounion`, and :rst:dir:`c:autoenum`
directives, their C++ domain counterparts, and the :rst:dir:`cpp:autoclass`
directive incorporate the documentation comments for the specified object in the
specified file, with additional control over the structure, class or union
members and enumeration constants to include.

The directives support all the same directive options as :rst:dir:`c:autodoc`,
:rst:dir:`c:autovar`, :rst:dir:`c:autotype`, :rst:dir:`c:automacro`, and
:rst:dir:`c:autofunction`, adding the ``members`` option.

.. rst:directive:: .. c:autostruct:: name
.. rst:directive:: .. cpp:autostruct:: name

   Incorporate the documentation comment for the structure ``name``, optionally
   including member documentation as specified by ``members``.

   The ``file`` option is as in :rst:dir:`c:autovar`. If ``file`` is specified,
   look up ``name`` there, otherwise look up ``name`` in all previously parsed
   files in the current document.

   .. rst:directive:option:: members
      :type: text

      The ``members`` option specifies the struct members to include:

      * If ``members`` is not present, do not include member documentation at
        all.

      * If ``members`` is specified without arguments, include all member
        documentation recursively.

      * If ``members`` is specified with a comma-separated list of arguments,
        include all specified member documentation recursively.

   For example:

   .. code-block:: rst

      .. c:autostruct:: example_struct
         :file: example_file.c

      .. c:autostruct:: example_struct
         :members:

      .. c:autostruct:: example_struct
         :members: member_one, member_two

.. rst:directive:: .. cpp:autoclass:: name

   Same as :rst:dir:`cpp:autostruct` but for classes.

   For example:

   .. code-block:: rst

      .. cpp:autoclass:: example_class
         :file: example_file.cpp
         :members: member_one, member_two

.. rst:directive:: .. c:autounion:: name
.. rst:directive:: .. cpp:autounion:: name

   Same as :rst:dir:`c:autostruct` but for unions.

   .. code-block:: rst

      .. c:autounion:: example_union
         :file: example_file.c
         :members: some_member

.. rst:directive:: .. c:autoenum:: name
.. rst:directive:: .. cpp:autoenum:: name

   Same as :rst:dir:`c:autostruct` but for enums. The enumeration constants are
   considered members and are included according to the ``members`` option.

   .. code-block:: rst

      .. c:autoenum:: example_enum
         :file: example_file.c
         :members:

      .. c:autoenum:: example_enum
         :members: CONSTANT_ONE, CONSTANT_TWO

Generic Documentation Sections
------------------------------

The :rst:dir:`c:autosection` and :rst:dir:`cpp:autosection` directives
incorporate generic documentation comments not attached to any objects in the
specified file.

.. rst:directive:: .. c:autosection:: name
.. rst:directive:: .. cpp:autosection:: name

   Incorporate the generic documentation comment identified by ``name``.

   The ``name`` is derived from the first sentence of the comment, and may
   contain whitespace. It starts from the first alphanumeric character,
   inclusive, and extends to the next ``:``, ``.``, or newline, non-inclusive.

   The ``file`` option is as in :rst:dir:`c:autovar`. If ``file`` is specified,
   look up ``name`` there, otherwise look up ``name`` in all previously parsed
   files in the current document.

   For example:

   .. code-block:: c

      /**
       * This is the reference. This is not. It all becomes
       * the documentation comment.
       */

   .. code-block:: rst

      .. c:autosection:: This is the reference
	 :file: example_file.c

   Note that the above does not automatically create hyperlink targets that you
   could reference from reStructuredText. However, reStructuredText hyperlink
   targets work nicely as the reference name for the directive:

   .. code-block:: c

      /**
       * .. _This is the reference:
       *
       * The actual documentation comment.
       *
       * You can use :ref:`This is the reference` to reference
       * this comment in reStructuredText.
       */

   .. code-block:: rst

      .. c:autosection:: This is the reference
	 :file: example_file.c
