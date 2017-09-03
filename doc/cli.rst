Command-Line Interface
======================

Synopsis
--------

**hawkmoth.py** [options] FILE

Description
-----------

In addition to the extension, Hawkmoth provides a command-line interface to the
parser, independent of Sphinx. This is used mainly for automated testing of the
parser parts.

**hawkmoth.py** prints the documentation comments extracted from FILE, along
with the generated C Domain directives, to standard output.

Supported options for **hawkmoth.py** include:

.. program:: hawkmoth.py

.. option:: FILE

   The C source or header file to parse.

.. option:: --compat=<option>

   Compatibility option. One of ``none`` (the default), ``javadoc-basic``,
   ``javadoc-liberal``, and ``kernel-doc``. This can be used to perform a
   limited conversion of Javadoc-style tags to reStructuredText.

.. option:: --clang=<params>

   A comma separated list of arguments to pass to ``clang`` while parsing the
   source, typically to define macros for conditional compilation, for example
   ``--clang=-DFOO=1,-DBAR=2``. No additional arguments are passed by default.

.. option:: -h

   Print help.

Exit Status
-----------

0 on success.

See Also
--------

**clang(1)**
