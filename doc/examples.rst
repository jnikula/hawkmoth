
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

.. literalinclude:: ../test/example-autodoc.c
   :language: C
   :caption: example-autodoc.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-autodoc.c

Output
~~~~~~

.. c:autodoc:: example-autodoc.c


Macro
-----

Source
~~~~~~

.. literalinclude:: ../test/example-macro.c
   :language: C
   :caption: example-macro.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-macro.c

Output
~~~~~~

.. c:autodoc:: example-macro.c


Directive
~~~~~~~~~

.. code-block:: rest

   .. c:automacro:: DIE
      :file: example-macro.c

Output
~~~~~~

.. c:namespace-push:: namespace_fc499782b4098eda1789721fd08742ba

.. c:automacro:: DIE
   :file: example-macro.c

.. c:namespace-pop::


Variable
--------

Source
~~~~~~

.. literalinclude:: ../test/example-variable.c
   :language: C
   :caption: example-variable.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-variable.c

Output
~~~~~~

.. c:autodoc:: example-variable.c


Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autovar:: meaning_of_life
      :file: example-variable.c

Output
~~~~~~

.. c:namespace-push:: namespace_238163a4c73047a60ccef522ea195193

.. c:autovar:: meaning_of_life
   :file: example-variable.c

.. c:namespace-pop::


Typedef
-------

Source
~~~~~~

.. literalinclude:: ../test/example-typedef.c
   :language: C
   :caption: example-typedef.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autotype:: list_data_t
      :file: example-typedef.c

Output
~~~~~~

.. c:autotype:: list_data_t
   :file: example-typedef.c


Enum
----

Source
~~~~~~

.. literalinclude:: ../test/example-enum.c
   :language: C
   :caption: example-enum.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autoenum:: mode
      :file: example-enum.c
      :members:

Output
~~~~~~

.. c:autoenum:: mode
   :file: example-enum.c
   :members:


Struct
------

Source
~~~~~~

.. literalinclude:: ../test/example-struct.c
   :language: C
   :caption: example-struct.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-struct.c

Output
~~~~~~

.. c:autodoc:: example-struct.c


Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autostruct:: list
      :file: example-struct.c
      :members:

Output
~~~~~~

.. c:namespace-push:: namespace_6719e1b2c4db0da6ad0361cea0c2742f

.. c:autostruct:: list
   :file: example-struct.c
   :members:

.. c:namespace-pop::


Union
-----

Source
~~~~~~

.. literalinclude:: ../test/example-autounion.c
   :language: C
   :caption: example-autounion.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autounion:: onion
      :file: example-autounion.c
      :members:

Output
~~~~~~

.. c:autounion:: onion
   :file: example-autounion.c
   :members:


Function
--------

Source
~~~~~~

.. literalinclude:: ../test/example-function.c
   :language: C
   :caption: example-function.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-function.c

Output
~~~~~~

.. c:autodoc:: example-function.c


Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autofunction:: frob
      :file: example-function.c

Output
~~~~~~

.. c:namespace-push:: namespace_c8d7b219201e168fc0ac126ec28e5dbf

.. c:autofunction:: frob
   :file: example-function.c

.. c:namespace-pop::


Preprocessor
------------

Source
~~~~~~

.. literalinclude:: ../test/example-preprocessor.c
   :language: C
   :caption: example-preprocessor.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-preprocessor.c
      :clang: -DDEEP_THOUGHT

Output
~~~~~~

.. c:autodoc:: example-preprocessor.c
   :clang: -DDEEP_THOUGHT


Transform
---------

Source
~~~~~~

.. literalinclude:: ../test/example-transform.c
   :language: C
   :caption: example-transform.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-transform.c
      :transform: napoleon

Output
~~~~~~

.. c:autodoc:: example-transform.c
   :transform: napoleon


Compat
------

Source
~~~~~~

.. literalinclude:: ../test/example-compat.c
   :language: C
   :caption: example-compat.c

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: example-compat.c
      :transform: javadoc-liberal

Output
~~~~~~

.. c:autodoc:: example-compat.c
   :transform: javadoc-liberal


