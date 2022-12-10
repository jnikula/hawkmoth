
The ``c:autodoc`` directive is the easiest way to extract all the
documentation comments from one or more source files in one go. The
other directives provide more fine-grained control over what to
document.

This example provides a brief overview of the most common features.

Note that the documentation comments below are **not** good examples
of how to document your code. Instead, the comments primarily
describe the features of Hawkmoth and Sphinx.

Source files may contain documentation comments not attached to any C
constructs. They will be included as generic documentation comments,
like this one.


.. c:macro:: ERROR

   Macro documentation.


.. c:struct:: foo

   Struct documentation.


   .. c:member:: const char *m1

      Member documentation.


   .. c:member:: int m2

      Member documentation.


.. c:enum:: bar

   Enum documentation.


   .. c:enumerator:: E1

      Enumeration constant documentation.


   .. c:enumerator:: E2

      Enumeration constant documentation.


.. c:function:: int baz(int p1, int p2)

   Function documentation.

   :param p1: Parameter documentation
   :param int p2: Parameter documentation with type
   :return: Return value documentation

