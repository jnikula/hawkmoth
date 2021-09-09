
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
   




Automacro
---------

Source
~~~~~~

.. literalinclude:: examples/example-11-automacro.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:automacro:: examples/example-11-automacro.c DIE
      

Output
~~~~~~

.. c:namespace-push:: Automacro

.. c:automacro:: examples/example-11-automacro.c DIE
   

.. c:namespace-pop::


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
   




Autovar
-------

Source
~~~~~~

.. literalinclude:: examples/example-21-autovar.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autovar:: examples/example-21-autovar.c meaning_of_life
      

Output
~~~~~~

.. c:namespace-push:: Autovar

.. c:autovar:: examples/example-21-autovar.c meaning_of_life
   

.. c:namespace-pop::


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
   




Autotype
--------

Source
~~~~~~

.. literalinclude:: examples/example-31-autotype.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autotype:: examples/example-31-autotype.c list_data_t
      

Output
~~~~~~

.. c:namespace-push:: Autotype

.. c:autotype:: examples/example-31-autotype.c list_data_t
   

.. c:namespace-pop::


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
   




Autoenum
--------

Source
~~~~~~

.. literalinclude:: examples/example-41-autoenum.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autoenum:: examples/example-41-autoenum.c mode
      

Output
~~~~~~

.. c:namespace-push:: Autoenum

.. c:autoenum:: examples/example-41-autoenum.c mode
   

.. c:namespace-pop::


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
   




Autostruct
----------

Source
~~~~~~

.. literalinclude:: examples/example-51-autostruct.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autostruct:: examples/example-51-autostruct.c list
      

Output
~~~~~~

.. c:namespace-push:: Autostruct

.. c:autostruct:: examples/example-51-autostruct.c list
   

.. c:namespace-pop::


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




Autofunction
------------

Source
~~~~~~

.. literalinclude:: examples/example-71-autofunction.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autofunction:: examples/example-71-autofunction.c frob
      

Output
~~~~~~

.. c:namespace-push:: Autofunction

.. c:autofunction:: examples/example-71-autofunction.c frob
   

.. c:namespace-pop::


Transform
---------

Source
~~~~~~

.. literalinclude:: examples/example-75-transform.c
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: examples/example-75-transform.c
      :transform: napoleon

Output
~~~~~~



.. c:autodoc:: examples/example-75-transform.c
   :transform: napoleon




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
      :transform: javadoc-liberal

Output
~~~~~~



.. c:autodoc:: examples/example-80-compat.c
   :transform: javadoc-liberal




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
   




