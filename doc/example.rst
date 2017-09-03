Example
=======

Input
-----

.. literalinclude:: example.c
   :language: C

Directive
---------

::

   .. c:autodoc:: example.c

Output
------

.. Using the only directive like this is *not* recommended for normal Hawkmoth
   usage.

.. only:: not have_hawkmoth

   .. warning:: The documentation was built without Hawkmoth and/or its
                dependencies (perhaps on https://readthedocs.org/) and thus the
                example output is not currently available.

.. c:autodoc:: example.c
