.. _built-in-extensions:

Built-In Extensions
===================

Hawkmoth is :ref:`extensible <extending>`, and ships with some built-in
extensions.

.. _hawkmoth.ext.javadoc:

hawkmoth.ext.javadoc
--------------------

This extension converts Javadoc_ comments to reStructuredText, using the
:event:`hawkmoth-process-docstring` event.

.. note::

   The Javadoc support is rudimentary at best.

.. _Javadoc: https://www.oracle.com/java/technologies/javase/javadoc.html

Installation and configuration in ``conf.py``:

.. code-block:: python

   extensions.append('hawkmoth.ext.javadoc')

.. py:data:: hawkmoth_javadoc_transform
   :type: str

   Name of the transformation to handle. Defaults to ``'javadoc'``. Only convert
   the comment if the ``transform`` option matches this name, otherwise do
   nothing. Usually there's no need to modify this option.

For example:

.. code-block:: python
   :caption: conf.py

   extensions.append('hawkmoth.ext.javadoc')
   hawkmoth_transform_default = 'javadoc'  # Transform everything

:data:`hawkmoth_transform_default` sets the default for the ``transform``
option.

.. code-block:: c
   :caption: file.c

   /**
    * The baznicator.
    *
    * @param foo The Foo parameter.
    * @param bar The Bar parameter.
    * @return 0 on success, non-zero error code on error.
    * @since v0.1
    */
   int baz(int foo, int bar);

.. code-block:: rst
   :caption: api.rst

   .. c:autofunction:: baz
      :file: file.c

.. _hawkmoth.ext.napoleon:

hawkmoth.ext.napoleon
---------------------

This extension provides a bridge from Hawkmoth to the
:external+sphinx:py:mod:`sphinx.ext.napoleon` extension, using the
:event:`hawkmoth-process-docstring` event, to support Napoleon style
documentation comments.

Installation and configuration in ``conf.py``:

.. code-block:: python

   extensions.append('hawkmoth.ext.napoleon')

.. py:data:: hawkmoth_napoleon_transform
   :type: str

   Name of the transformation to handle. Defaults to ``'napoleon'``. Only
   convert the comment if the ``transform`` option matches this name, otherwise
   do nothing. Usually there's no need to modify this option.

For example:

.. code-block:: python
   :caption: conf.py

   extensions.append('hawkmoth.ext.napoleon')
   # Uncomment to transform everything, example below uses :transform: option
   # hawkmoth_transform_default = 'napoleon'

.. code-block:: c
   :caption: file.c

   /**
    * The baznicator.
    *
    * Args:
    *     foo: The Foo parameter.
    *     bar: The Bar parameter.
    *
    * Returns:
    *     0 on success, non-zero error code on error.
    */
   int baz(int foo, int bar);

.. code-block:: rst
   :caption: api.rst

   .. c:autofunction:: baz
      :file: file.c
      :transform: napoleon

.. _hawkmoth.ext.transformations:

hawkmoth.ext.transformations
----------------------------

This extension handles the :py:data:`cautodoc_transformations` feature, using
the :event:`hawkmoth-process-docstring` event.

.. note::

   Going forward, it's recommended to handle transformations using the event
   directly instead of :py:data:`cautodoc_transformations`. This built-in
   extension provides backward compatibility for the functionality.

   For now, this extension is loaded by default, and the installation step below
   is not strictly necessary. This will change in the future.

Installation and configuration in ``conf.py``:

.. code-block:: python

   extensions.append('hawkmoth.ext.transformations')

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
