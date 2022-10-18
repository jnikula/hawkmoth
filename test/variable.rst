
.. c:var:: int sheesh

   This is a variable document.


.. c:var:: int (*function_pointer_variable)(int *param_name_ignored)

   function pointer variable


.. c:var:: int (*variadic_function_pointer_variable)(int *param_name_ignored, ...)

   variadic function pointer variable


.. c:var:: int (**pointer_to_function_pointer_variable)(int)

   pointer to function pointer variable


.. c:var:: void (*function_pointer_array[5])(void)

   array of function pointers


.. c:var:: void (*array_of_function_pointer_array[5][15])(void)

   array of array of function pointers


.. c:var:: const char *(*const function_pointer_with_qualifier)(const char *in)

   function pointer with lots of const qualifiers


.. c:var:: const char *(*const volatile function_pointer_with_multiple_qualifiers)(const char *in)

   function pointer with multiple qualifiers


.. c:var:: const char *(*const*volatile*restrict legal_type_involving_function_pointer[12][3])(const char *in)

   a complex type involving function pointers somehow


.. c:var:: int (*function_pointer_with_function_pointer_arg)( float (*arg1)(char c))

   function pointer to a function taking a function pointer as arg


.. c:var:: char *array_of_pointers[1]

   Array of pointers.


.. c:var:: int multi_dim[1][2]

   Multi-dimensional array.

