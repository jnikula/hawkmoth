
.. c:macro:: SAMPLE_MACRO

   macro with trailing comment


.. c:macro:: FUNCTION_MACRO(a, b)

   function-like macro with trailing comment


.. c:macro:: MULTILINE_MACRO(a, b)

   multiline macro with trailing comment


.. cpp:var:: int leading_comment_with_trailing_marker

   leading comment with a trailing comment marker ///< should not be treated as a trailing comment


.. cpp:var:: int leading_comment_with_trailing_marker2

   ///< trailing comment marker at beginning of line


.. cpp:enum:: sample_enum

   enum trailing comment for c style enum


   .. cpp:enumerator:: VALUE_ONE

      enum value with trailing comment


   .. cpp:enumerator:: VALUE_TWO

      another enum value with trailing comment


   .. cpp:enumerator:: VALUE_THREE

      yet another enum value with trailing comment


.. cpp:enum:: sample_enum2

   trailing comment for c++ style enum


   .. cpp:enumerator:: VALUE_FOUR

      another enum value with trailing comment


   .. cpp:enumerator:: VALUE_FIVE

      yet another enum value with trailing comment


.. cpp:enum-class:: sample_enum3

   trailing comment for c++ enum class


   .. cpp:enumerator:: VALUE_SIX

      enum class value with trailing comment


   .. cpp:enumerator:: VALUE_SEVEN

      another enum class value with trailing comment


.. cpp:union:: sample_union

   union trailing comment


   .. cpp:member:: int int_value

      union member with trailing comment


   .. cpp:member:: float float_value

      another union member with trailing comment


.. cpp:union:: sample_union2

   trailing comment for c++ style union


   .. cpp:member:: int int_value2

      union member with trailing comment


   .. cpp:member:: double double_value

      another union member with trailing comment


.. cpp:struct:: sample_struct

   trailing comment for struct


   .. cpp:member:: public int trailing1

      trailing comment for member


   .. cpp:member:: public double trailing2

      trailing comment only


   .. cpp:member:: public void *trailing3

      trailing comment


.. cpp:struct:: sample_struct2

   trailing comment for c++ style struct


   .. cpp:member:: public int trailing1

      trailing comment for member


   .. cpp:member:: public double trailing2

      trailing comment only


   .. cpp:member:: public void *trailing3

      trailing comment


.. cpp:class:: SampleClass

   class with trailing comment


   .. cpp:member:: public int member1

      class member with trailing comment


   .. cpp:member:: public double member2

      another class member with trailing comment


   .. cpp:member:: public struct InnerStruct inner

      trailing comment for inner struct member


   .. cpp:struct:: InnerStructType

      trailing comment for nested struct type


      .. cpp:member:: public int inner_member2

         inner struct member with trailing comment


   .. cpp:function:: private void private_function(void)

      private helper function with trailing comment


   .. cpp:member:: private int private_variable

      private variable with trailing comment


.. cpp:type:: void (*sample_func_ptr)(int )

   typedef with trailing comment


.. cpp:type:: sample_func_ptr_alias = sample_func_ptr

   using alias with trailing comment


.. cpp:function:: int sample_func(int a, int b)

   function with trailing comment after line


.. cpp:function:: int sample_func2(int a, int b)

   function with trailing comment after block


.. cpp:function:: int sample_func3(int a, int b)

   function with trailing comment before parameters


.. cpp:function:: int sample_func4(int a, int b)

   function declaration with trailing comment


.. cpp:var:: int tester

   trailing comment 1


.. cpp:var:: int tester2

   This leading comment should still apply


.. cpp:var:: int tester3

   trailing comment at end of file

