.. _troubleshooting:

Troubleshooting
===============

Things not working? Here are some things to try isolate the problem.

Use the parser directly
-----------------------

Hawkmoth comes with a command-line debug tool to extract the documentation
comments from source without Sphinx. This can be useful in figuring out if the
problem is in the parser or in the Sphinx extension.

.. code-block:: shell

   hawkmoth path/to/file.c

See the help for command-line options:

.. code-block:: shell

   hawkmoth --help

Get verbose output from Sphinx
------------------------------

Pass the ``-v`` option to ``sphinx-build`` to get more verbose output, and see
if anything stands out.

.. code-block:: shell

   sphinx-build -v SOURCEDIR OUTPUTDIR

or

.. code-block:: shell

   make SPHINXOPTS=-v html

You can also use ``-vv`` for even more verbose output.
