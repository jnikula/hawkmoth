
.. c:function:: static inline int foo(int bar, int baz)

   Foo function.


.. c:function:: bool boolean(bool bar, bool baz)

   Bool function.


.. c:function:: int no_parameters(void)

   No parameters.


.. c:function:: int empty_parameter_list()

   Empty parameter list.


.. c:function:: int variadic(const char *fmt, ...)

   Variadic function.


.. c:function:: void foorray(const double array[], int x[5])

   Array parameters.


.. c:function:: void multi_array_param(int x[2][2], int y[2][2])

   Array parameters with multiple dimensions.

   Clang removes spaces.


.. c:function:: void function_pointer_param(void *(*hook)(void *p, int n))

   Function pointer parameter.


.. c:function:: void array_of_pointer_params(char *p[])

   Array of pointers parameter.

