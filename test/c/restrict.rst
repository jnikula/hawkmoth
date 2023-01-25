
.. c:var:: int *restrict restrict_ptr

   'restrict' pointer.


.. c:var:: const int *const restrict *restrict slightly_weirder_ptr[4][2]

   A weirder pointer.


.. c:var:: const char *(*const *volatile *restrict legal_type_involving_function_pointer[12][3])(const char *restrict in)

   A complex pointer type that is only legal in C.


.. c:function:: int picky_function(const char *restrict not_your_avg_ptr)

   Function with heavily qualified argument.

