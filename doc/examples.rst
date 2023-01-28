
.. Generated using update-examples, do not edit manually!

.. _examples:

Examples
========

This page showcases Hawkmoth in action.

.. contents::
   :local:
   :depth: 1

.. only:: not have_hawkmoth

   .. note:: The documentation you are viewing was built without Hawkmoth and/or
             its dependencies (perhaps on https://readthedocs.org/). The output
             seen below was pre-generated statically using Hawkmoth, and should
             closely reflect actual results.

Overview
--------

Source
~~~~~~

.. literalinclude:: ../test/examples/autodoc.c
   :language: C
   :caption: autodoc.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: autodoc.c

Output
~~~~~~

.. c:autodoc:: autodoc.c


Variable
--------

Source
~~~~~~

.. literalinclude:: ../test/examples/variable.c
   :language: C
   :caption: variable.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: variable.c

Output
~~~~~~

.. c:autodoc:: variable.c


Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autovar:: meaning_of_life
      :file: variable.c

Output
~~~~~~

.. c:namespace-push:: namespace_examples_autovar

.. c:autovar:: meaning_of_life
   :file: variable.c

.. c:namespace-pop::


Typedef
-------

Source
~~~~~~

.. literalinclude:: ../test/examples/typedef.c
   :language: C
   :caption: typedef.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autotype:: list_data_t
      :file: typedef.c

Output
~~~~~~

.. c:autotype:: list_data_t
   :file: typedef.c


Macro
-----

Source
~~~~~~

.. literalinclude:: ../test/examples/macro.c
   :language: C
   :caption: macro.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: macro.c

Output
~~~~~~

.. c:autodoc:: macro.c


Directive
~~~~~~~~~

.. code-block:: rest

   .. c:automacro:: DIE
      :file: macro.c

Output
~~~~~~

.. c:namespace-push:: namespace_examples_automacro

.. c:automacro:: DIE
   :file: macro.c

.. c:namespace-pop::


Function
--------

Source
~~~~~~

.. literalinclude:: ../test/examples/function.c
   :language: C
   :caption: function.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: function.c

Output
~~~~~~

.. c:autodoc:: function.c


Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autofunction:: frob
      :file: function.c

Output
~~~~~~

.. c:namespace-push:: namespace_examples_autofunction

.. c:autofunction:: frob
   :file: function.c

.. c:namespace-pop::


Struct
------

Source
~~~~~~

.. literalinclude:: ../test/examples/struct.c
   :language: C
   :caption: struct.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: struct.c

Output
~~~~~~

.. c:autodoc:: struct.c


Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autostruct:: list
      :file: struct.c
      :members:

Output
~~~~~~

.. c:namespace-push:: namespace_examples_autostruct

.. c:autostruct:: list
   :file: struct.c
   :members:

.. c:namespace-pop::


Union
-----

Source
~~~~~~

.. literalinclude:: ../test/examples/autounion.c
   :language: C
   :caption: autounion.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autounion:: onion
      :file: autounion.c
      :members:

Output
~~~~~~

.. c:autounion:: onion
   :file: autounion.c
   :members:


Enum
----

Source
~~~~~~

.. literalinclude:: ../test/examples/enum.c
   :language: C
   :caption: enum.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autoenum:: mode
      :file: enum.c
      :members:

Output
~~~~~~

.. c:autoenum:: mode
   :file: enum.c
   :members:


Preprocessor
------------

Source
~~~~~~

.. literalinclude:: ../test/examples/preprocessor.c
   :language: C
   :caption: preprocessor.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: preprocessor.c
      :clang: -DDEEP_THOUGHT

Output
~~~~~~

.. c:autodoc:: preprocessor.c
   :clang: -DDEEP_THOUGHT


Transform
---------

Source
~~~~~~

.. literalinclude:: ../test/examples/transform.c
   :language: C
   :caption: transform.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: transform.c
      :transform: napoleon

Output
~~~~~~

.. c:autodoc:: transform.c
   :transform: napoleon


Compat
------

Source
~~~~~~

.. literalinclude:: ../test/examples/compat.c
   :language: C
   :caption: compat.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: compat.c
      :transform: javadoc

Output
~~~~~~

.. c:autodoc:: compat.c
   :transform: javadoc


