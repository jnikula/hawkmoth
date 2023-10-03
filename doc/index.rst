Hawkmoth -- Sphinx Autodoc for C and C++
========================================

Hawkmoth is a Sphinx_ extension to incorporate C and C++ source code comments
formatted in reStructuredText_ into Sphinx based documentation. It uses Clang_
Python Bindings for parsing, and generates :external+sphinx:doc:`C
<usage/domains/c>` and :external+sphinx:doc:`C++ <usage/domains/cpp>` domain
directives for C and C++ documentation, respectively. In short, Hawkmoth is
Sphinx Autodoc for C/C++.

Hawkmoth aims to be a compelling alternative for documenting C and C++ projects
using Sphinx, mainly through its simplicity of design, implementation and use.

.. note::

   The C++ support is still in early stages of development, and lacks some
   fundamental features such as handling namespaces and documenting C++ specific
   features other than classes.

Please see the `Hawkmoth project GitHub page`_ (or README.rst in the source
repository) for information on how to obtain, install, and contribute to
Hawkmoth, as well as how to contact the developers.

Read on for information about Hawkmoth installation details and usage; how to
configure and use the extension and how to write documentation comments, with
examples.

.. _Sphinx: https://www.sphinx-doc.org

.. _reStructuredText: https://docutils.sourceforge.io/rst.html

.. _Clang: https://clang.llvm.org/

.. _Hawkmoth project GitHub page: https://github.com/jnikula/hawkmoth

Contents:

.. toctree::
   :maxdepth: 2

   Introduction <self>
   installation
   extension
   directives
   syntax
   examples
   extending
   built-in-extensions
   troubleshooting

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
