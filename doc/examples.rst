
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

.. literalinclude:: ../test/example-10-macro.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-10-macro.c
   

Output
~~~~~~

.. c:autodoc:: example-10-macro.c


Variable
--------

Source
~~~~~~

.. literalinclude:: ../test/example-20-variable.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-20-variable.c
   

Output
~~~~~~

.. c:autodoc:: example-20-variable.c


Typedef
-------

Source
~~~~~~

.. literalinclude:: ../test/example-30-typedef.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-30-typedef.c
   

Output
~~~~~~

.. c:autodoc:: example-30-typedef.c


Enum
----

Source
~~~~~~

.. literalinclude:: ../test/example-40-enum.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-40-enum.c
   

Output
~~~~~~

.. c:autodoc:: example-40-enum.c


Struct
------

Source
~~~~~~

.. literalinclude:: ../test/example-50-struct.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-50-struct.c
   

Output
~~~~~~

.. c:autodoc:: example-50-struct.c


Function
--------

Source
~~~~~~

.. literalinclude:: ../test/example-70-function.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-70-function.c
   

Output
~~~~~~

.. c:autodoc:: example-70-function.c


Preprocessor
------------

Source
~~~~~~

.. literalinclude:: ../test/example-70-preprocessor.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-70-preprocessor.c
      :clang: -DDEEP_THOUGHT
   

Output
~~~~~~

.. c:autodoc:: example-70-preprocessor.c
   :clang: -DDEEP_THOUGHT


Transform
---------

Source
~~~~~~

.. literalinclude:: ../test/example-75-transform.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-75-transform.c
      :transform: napoleon
   

Output
~~~~~~

.. c:autodoc:: example-75-transform.c
   :transform: napoleon


Compat
------

Source
~~~~~~

.. literalinclude:: ../test/example-80-compat.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-80-compat.c
      :transform: javadoc-liberal
   

Output
~~~~~~

.. c:autodoc:: example-80-compat.c
   :transform: javadoc-liberal


Generic
-------

Source
~~~~~~

.. literalinclude:: ../test/example-90-generic.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-90-generic.c
   

Output
~~~~~~

.. c:autodoc:: example-90-generic.c


