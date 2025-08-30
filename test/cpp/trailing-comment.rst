
.. c:macro:: SAMPLE_MACRO

   macro


.. c:macro:: FUNCTION_MACRO(a, b)

   function-like macro


.. cpp:enum:: sample_enum

   Documented enum


   .. cpp:enumerator:: VALUE_ONE

      enumerator 1


   .. cpp:enumerator:: VALUE_TWO

      enumerator 2


   .. cpp:enumerator:: VALUE_THREE

      enumerator 3


.. cpp:union:: sample_union

   Documented union


   .. cpp:member:: int int_value

      union member 1


   .. cpp:member:: float float_value

      union member 2


.. cpp:struct:: sample_struct

   Documented struct


   .. cpp:member:: public int trailing1

      struct member 1


   .. cpp:member:: public double trailing2

      struct member 2


   .. cpp:member:: public void *trailing3

      struct member 3


.. cpp:struct:: outer_struct

   Documented compound struct


   .. cpp:member:: public int outer

      outer member


   .. cpp:struct:: inner_struct

      inner struct type


      .. cpp:member:: public int innerb

         inner member


.. cpp:class:: sample_class

   Documented class


   .. cpp:member:: public int member1

      class member 1


   .. cpp:member:: public double member2

      class member 2


   .. cpp:member:: public void *member3

      class member 3


   .. cpp:function:: public int method(int a)

      class method


   .. cpp:member:: private int private_member

      private member


.. cpp:type:: void (*sample_func_ptr)(int )

   function typedef


.. cpp:function:: int fxn(int a, int b)

   function declaration


.. cpp:var:: int eof_variable

   trailing comment at end of file

