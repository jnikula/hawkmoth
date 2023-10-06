
.. cpp:var:: static int sheesh

   This is a variable document.


.. cpp:var:: static bool convert_bool

   Retain bool instead of using _Bool.


.. cpp:var:: static bool convert_Bool

   Also convert _Bool to bool.


.. cpp:var:: int (*function_pointer_variable)(int *param_name_ignored)

   function pointer variable


.. cpp:var:: int (*variadic_function_pointer_variable)(int *param_name_ignored, ...)

   variadic function pointer variable


.. cpp:var:: int (**pointer_to_function_pointer_variable)(int)

   pointer to function pointer variable


.. cpp:var:: void (*function_pointer_array[5])(void)

   array of function pointers


.. cpp:var:: void (*array_of_function_pointer_array[5][15])(void)

   array of array of function pointers


.. cpp:var:: const char *(*const function_pointer_with_qualifier)(const char *in)

   function pointer with lots of const qualifiers


.. cpp:var:: const char *(*const volatile function_pointer_with_multiple_qualifiers)(const char *in)

   function pointer with multiple qualifiers


.. cpp:var:: const char *(*const *volatile *const legal_type_involving_function_pointer[2][2])(const char *in)

   a complex type involving function pointers somehow


.. cpp:var:: int (*function_pointer_with_function_pointer_arg)( float (*arg1)(char c))

   function pointer to a function taking a function pointer as arg


.. cpp:var:: char *array_of_pointers[1]

   Array of pointers.


.. cpp:var:: extern int multi_dim[1][2]

   Multi-dimensional array.

