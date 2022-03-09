
.. cpp:function:: static inline int foo(int bar, int baz)

   Foo function.


.. cpp:function:: bool boolean(bool bar, bool baz)

   Bool function.


.. cpp:function:: int no_parameters(void)

   No parameters.


.. cpp:function:: int empty_parameter_list(void)

   Empty parameter list.


.. cpp:function:: int variadic(const char *fmt, ...)

   Variadic function.


.. cpp:function:: void foorray(const double array[], int x[5])

   Array parameters.


.. cpp:function:: void multi_array_param(int x[2][2], int y[2][2])

   Array parameters with multiple dimensions.

   Clang removes spaces.


.. cpp:function:: void function_pointer_param(void *(*hook)(void *p, int n))

   Function pointer parameter.


.. cpp:function:: void array_of_pointer_params(char *p[])

   Array of pointers parameter.

