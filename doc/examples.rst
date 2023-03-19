
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

.. literalinclude:: ../test/examples/overview.c
   :language: C
   :caption: overview.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: overview.c

Output
~~~~~~

.. c:autodoc:: overview.c


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


Class
-----

Source
~~~~~~

.. literalinclude:: ../test/examples/class.cpp
   :language: C
   :caption: class.cpp

Directive
~~~~~~~~~

.. code-block:: rest

   .. cpp:autoclass:: Circle
      :file: class.cpp
      :members:

Output
~~~~~~

.. cpp:autoclass:: Circle
   :file: class.cpp
   :members:


Union
-----

Source
~~~~~~

.. literalinclude:: ../test/examples/union.c
   :language: C
   :caption: union.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autounion:: onion
      :file: union.c
      :members:

Output
~~~~~~

.. c:autounion:: onion
   :file: union.c
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


Napoleon-style comments
-----------------------

Source
~~~~~~

.. literalinclude:: ../test/examples/napoleon.c
   :language: C
   :caption: napoleon.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: napoleon.c
      :transform: napoleon

Output
~~~~~~

.. c:autodoc:: napoleon.c
   :transform: napoleon


Javadoc-style comments
----------------------

Source
~~~~~~

.. literalinclude:: ../test/examples/javadoc.c
   :language: C
   :caption: javadoc.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: javadoc.c
      :transform: javadoc

Output
~~~~~~

.. c:autodoc:: javadoc.c
   :transform: javadoc


