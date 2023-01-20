.. _built-in-extensions:

Built-In Extensions
===================

Hawkmoth is :ref:`extensible <extending>`, and ships with some built-in
extensions.

.. _hawkmoth.ext.javadoc:

hawkmoth.ext.javadoc
--------------------

This extension converts Javadoc_ comments to reStructuredText.

.. _Javadoc: https://www.oracle.com/technetwork/java/javase/documentation/javadoc-137458.html

Installation and configuration in ``conf.py``:

.. code-block:: python

   extensions.append('hawkmoth.ext.javadoc')

.. py:data:: hawkmoth_javadoc_transform
   :type: list

   List of transforms to convert, defaults to ``['javadoc']``. If the
   ``transform`` option is not in in this list, do nothing.

.. _hawkmoth.ext.transformations:

hawkmoth.ext.transformations
----------------------------

This extension handles the :py:data:`cautodoc_transformations` feature, using
the :event:`hawkmoth-process-docstring` event.

Going forward, it's recommended to handle transformations using the event
directly instead of :py:data:`cautodoc_transformations`. This built-in extension
provides backward compatibility for the functionality.

Installation and configuration in ``conf.py``:

.. code-block:: python

   extensions.append('hawkmoth.ext.transformations')

For now, this extension is loaded by default, and the above is not strictly
necessary. This may change in the future.

.. py:data:: cautodoc_transformations
   :type: dict

   Transformation functions for the :rst:dir:`c:autodoc` directive ``transform``
   option. This is a dictionary that maps names to functions. The names can be
   used in the directive ``transform`` option. The functions are expected to
   take a (multi-line) comment string as a parameter, and return the transformed
   string. This can be used to perform custom conversions of the comments,
   including, but not limited to, Javadoc-style compat conversions.

   The special key ``None``, if present, is used to convert everything, unless
   overridden in the directive ``transform`` option. The special value ``None``
   means no transformation is to be done.

   For example, this configuration would transform everything using
   ``default_transform`` function by default, unless overridden in the directive
   ``transform`` option with ``javadoc`` or ``none``. The former would use
   ``javadoc_transform`` function, and the latter would bypass transform
   altogether.

   .. code-block:: python

      cautodoc_transformations = {
          None: default_transform,
          'javadoc': javadoc_transform,
          'none': None,
      }

   The example below shows how to use Hawkmoth's existing compat functions in
   ``conf.py``.

   .. code-block:: python

      from hawkmoth.util import doccompat
      cautodoc_transformations = {
          'javadoc-basic': doccompat.javadoc,
          'javadoc-liberal': doccompat.javadoc_liberal,
          'kernel-doc': doccompat.kerneldoc,
      }

Converting to Event Handling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have a function ``foo_transform()`` that you use with
:py:data:`cautodoc_transformations`, it can be used with the
:event:`hawkmoth-process-docstring` event as follows in ``conf.py``.

Before:

.. code-block:: python

   cautodoc_transformations = {
       'foo': foo_transform
   }

After:

.. code-block:: python

   def _process_docstring(app, lines, transform, options):
       if transform != 'foo':
           return

       comment = '\n.join(lines)
       comment = foo_transform(comment)
       lines[:] = comment.splitlines()[:]

   # conf.py can be turned into an extension by adding setup() function
   setup(app)
       app.connect('hawkmoth-process-docstring', _process_docstring)

Of course, if you modify ``foo_transform()`` to operate on a list of strings,
you can do away with the ``join()`` and ``splitlines()`` pair. Also, this can be
turned into a proper Sphinx extension by putting it in a separate package. See
:external+sphinx:doc:`development/index` for details.
