.. _directives:

Directives
==========

Hawkmoth provides several new directives for incorporating :ref:`documentation
comments <syntax>` from C source files into the reStructuredText document. There
are three main types of directives, for incorporating documentation from entire
files, for single objects, and for composite objects optionally with members.

Source Files
------------

The :rst:dir:`c:autodoc` directive simply includes all the documentation
comments from any number of files. This is the most basic and quickest way to
generate documentation, but offers no control over what gets included.

.. rst:directive:: .. c:autodoc:: filename-pattern [...]

   Incorporate documentation comments from the files specified by the space
   separated list of filename patterns given as arguments. The patterns are
   interpreted relative to the :data:`hawkmoth_root` configuration option.

   .. rst:directive:option:: transform
      :type: text

      Override :data:`hawkmoth_transform_default` for the ``transform``
      parameter value of the :event:`hawkmoth-process-docstring` event.

      See also :ref:`hawkmoth.ext.transformations`.

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
:rst:dir:`c:autofunction` directives incorporate the documentation comment for
the specified object in the specified file.

The directives support all the same directive options as :rst:dir:`c:autodoc`,
adding the ``file`` option.

.. rst:directive:: .. c:autovar:: name

   Incorporate the documentation comment for the variable ``name`` in the file
   ``file``.

   .. rst:directive:option:: file
      :type: text

      The ``file`` option specifies to file to parse. The filename is
      interpreted relative to the :data:`hawkmoth_root` configuration
      option. (For the time being, this option is mandatory.)

   For example:

   .. code-block:: rst

      .. c:autovar:: example_variable
         :file: example_file.c

.. rst:directive:: .. c:autotype:: name

   Same as :rst:dir:`c:autovar` but for typedefs.

   .. code-block:: rst

      .. c:autotype:: example_type_t
         :file: example_file.c

.. rst:directive:: .. c:automacro:: name

   Same as :rst:dir:`c:autovar` but for macros, including function-like macros.

   .. code-block:: rst

      .. c:automacro:: EXAMPLE_MACRO
         :file: example_file.c

.. rst:directive:: .. c:autofunction:: name

   Same as :rst:dir:`c:autovar` but for functions. (Use :rst:dir:`c:automacro`
   for function-like macros.)

   .. code-block:: rst

      .. c:autofunction:: example_function
         :file: example_file.c

Structures, Unions, and Enumerations
------------------------------------

The :rst:dir:`c:autostruct`, :rst:dir:`c:autounion`, and :rst:dir:`c:autoenum`
directives incorporate the documentation comments for the specified object in
the specified file, with additional control over the structure or union members
and enumeration constants to include.

The directives support all the same directive options as :rst:dir:`c:autodoc`,
:rst:dir:`c:autovar`, :rst:dir:`c:autotype`, :rst:dir:`c:automacro`, and
:rst:dir:`c:autofunction`, adding the ``members`` option.

.. rst:directive:: .. c:autostruct:: name

   Incorporate the documentation comment for the structure ``name`` in the file
   ``file``, optionally including member documentation as specified by
   ``members``.

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
         :file: example_file.c
         :members:

      .. c:autostruct:: example_struct
         :file: example_file.c
         :members: member_one, member_two

.. rst:directive:: .. c:autounion:: name

   Same as :rst:dir:`c:autostruct` but for unions.

   .. code-block:: rst

      .. c:autounion:: example_union
         :file: example_file.c
         :members: some_member

.. rst:directive:: .. c:autoenum:: name

   Same as :rst:dir:`c:autostruct` but for enums. The enumeration constants are
   considered members and are included according to the ``members`` option.

   .. code-block:: rst

      .. c:autoenum:: example_enum
         :file: example_file.c
         :members:

      .. c:autoenum:: example_enum
         :file: example_file.c
         :members: CONSTANT_ONE, CONSTANT_TWO

Text Documentation Comments
---------------------------

.. rst:directive:: .. c:autotext:: name

   Incorporate the text documentation comment identified by ``name`` in the file
   ``file``. The ``file`` option is as in :rst:dir:`c:autovar`.

   The ``name`` is derived from the first sentence of the comment, and may
   contain whitespace. It starts from the first alphanumeric character,
   inclusive, and extends to the next ``:``, ``.``, or newline, non-inclusive.

   For example:

   .. code-block:: c

      /**
       * This is the reference. This is not.
       */

   .. code-block:: rst

      .. c:autotext:: This is the reference
	 :file: example_file.c

   reStructuredText hyperlink targets work nicely:

   .. code-block:: c

      /**
       * .. _This is the reference:
       */

   .. code-block:: rst

      .. c:autotext:: This is the reference
	 :file: example_file.c
