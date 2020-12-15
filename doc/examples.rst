
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

Macro
-----

Source
~~~~~~

.. literalinclude:: examples/example-10-macro.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: examples/example-10-macro.c
      

Output
~~~~~~

.. c:autodoc:: examples/example-10-macro.c
   

Variable
--------

Source
~~~~~~

.. literalinclude:: examples/example-20-variable.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: examples/example-20-variable.c
      

Output
~~~~~~

.. c:autodoc:: examples/example-20-variable.c
   

Typedef
-------

Source
~~~~~~

.. literalinclude:: examples/example-30-typedef.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: examples/example-30-typedef.c
      

Output
~~~~~~

.. c:autodoc:: examples/example-30-typedef.c
   

Enum
----

Source
~~~~~~

.. literalinclude:: examples/example-40-enum.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: examples/example-40-enum.c
      

Output
~~~~~~

.. c:autodoc:: examples/example-40-enum.c
   

Struct
------

Source
~~~~~~

.. literalinclude:: examples/example-50-struct.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: examples/example-50-struct.c
      

Output
~~~~~~

.. c:autodoc:: examples/example-50-struct.c
   

Function
--------

Source
~~~~~~

.. literalinclude:: examples/example-70-function.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: examples/example-70-function.c
      

Output
~~~~~~

.. c:autodoc:: examples/example-70-function.c
   

Preprocessor
------------

Source
~~~~~~

.. literalinclude:: examples/example-70-preprocessor.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: examples/example-70-preprocessor.c
      :clang: -DDEEP_THOUGHT

Output
~~~~~~

.. c:autodoc:: examples/example-70-preprocessor.c
   :clang: -DDEEP_THOUGHT

Compat
------

Source
~~~~~~

.. literalinclude:: examples/example-80-compat.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: examples/example-80-compat.c
      :compat: javadoc-liberal

Output
~~~~~~

.. c:autodoc:: examples/example-80-compat.c
   :compat: javadoc-liberal

Generic
-------

Source
~~~~~~

.. literalinclude:: examples/example-90-generic.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: examples/example-90-generic.c
      

Output
~~~~~~

.. c:autodoc:: examples/example-90-generic.c
   

