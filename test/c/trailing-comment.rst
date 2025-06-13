
.. c:macro:: SAMPLE_MACRO

   macro with trailing comment


.. c:macro:: FUNCTION_MACRO(a, b)

   function-like macro with trailing comment


.. c:macro:: MULTILINE_MACRO(a, b)

   multiline macro with trailing comment


.. c:var:: int leading_comment_with_trailing_marker

   leading comment with a trailing comment marker ///< should not be treated as a trailing comment


.. c:var:: int leading_comment_with_trailing_marker2

   ///< trailing comment marker at beginning of line


.. c:enum:: sample_enum

   enum trailing comment


   .. c:enumerator:: VALUE_ONE

      enum value with trailing comment


   .. c:enumerator:: VALUE_TWO

      another enum value with trailing comment


   .. c:enumerator:: VALUE_THREE

      yet another enum value with trailing comment


.. c:union:: sample_union

   union trailing comment


   .. c:member:: int int_value

      union member with trailing comment


   .. c:member:: float float_value

      another union member with trailing comment


.. c:struct:: sample_struct

   trailing comment for struct


   .. c:member:: int trailing1

      trailing comment for member


   .. c:member:: double trailing2

      trailing comment only


   .. c:member:: void *trailing3

      trailing comment


.. c:struct:: sample_struct_2

   trailing doc comment for outer struct


   .. c:struct:: inner_struct

      leading comment for inner struct type


      .. c:member:: int innerb

         inner trailing comment, prior not documented


   .. c:member:: struct inner_struct a

      trailing doc comment for inner struct member


.. c:type:: void (*sample_func_ptr)(int )

   typedef with trailing comment


.. c:function:: int sample_func(int a, int b)

   function with trailing comment after line


.. c:function:: int sample_func2(int a, int b)

   function with trailing comment after block


.. c:function:: int sample_func3(int a, int b)

   function with trailing comment before parameters


.. c:function:: int sample_func4(int a, int b)

   function declaration with trailing comment


.. c:var:: int tester

   trailing comment 1


.. c:var:: int tester2

   This leading comment should still apply


.. c:var:: int tester3

   trailing comment at end of file

