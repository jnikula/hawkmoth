.. SPDX-FileCopyrightText: 2023 Jani Nikula <jani@nikula.org>
.. SPDX-License-Identifier: BSD-2-Clause

.. _extending:

Extending
=========

Hawkmoth is a Sphinx extension that can be further extended with other Sphinx
extensions.

Events
------

See :external+sphinx:py:meth:`sphinx.application.Sphinx.connect` on how to
connect events.

.. event:: hawkmoth-process-docstring

   .. py:function:: func(app, lines, transform, options)
      :noindex:

      :param app: The Sphinx application object
      :type app: :external+sphinx:py:class:`sphinx.application.Sphinx`
      :param list[str] lines: The comment being processed
      :param str transform: Transformation
      :param dict options: The directive options

   This is similar to the :external+sphinx:event:`autodoc-process-docstring`
   event in the :external+sphinx:py:mod:`sphinx.ext.autodoc` extension.

   The *lines* argument is the documentation comment, with the comment markers
   removed, as a list of strings that the event handler may modify in-place.

   The *transform* argument is the ``transform`` option of the :ref:`directive
   <directives>` being processed, defaulting to
   :data:`hawkmoth_transform_default`, which defaults to ``None``. The event
   handler may use this to decide what, if anything, should be done to *lines*.

   The *options* argument is a dictionary with all the options given to the
   directive being processed.

   .. note::

      Please note that this API is still somewhat experimental and in
      development. In particular, new arguments may be added in the future.
