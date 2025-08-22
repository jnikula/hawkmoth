
.. c:macro:: SAMPLE_MACRO

   macro


.. c:macro:: FUNCTION_MACRO(a, b)

   function-like macro


.. c:enum:: sample_enum

   Documented enum


   .. c:enumerator:: VALUE_ONE

      enumerator 1


   .. c:enumerator:: VALUE_TWO = 1

      enumerator 2


   .. c:enumerator:: VALUE_THREE = 2

      enumerator 3


.. c:union:: sample_union

   Documented union


   .. c:member:: int int_value

      union member 1


   .. c:member:: float float_value

      union member 2


.. c:struct:: sample_struct

   Documented struct


   .. c:member:: int trailing1

      struct member 1


   .. c:member:: double trailing2

      struct member 2


   .. c:member:: void *trailing3

      struct member 3


.. c:struct:: outer_struct

   Documented compound struct


   .. c:member:: int outer

      outer member


   .. c:struct:: inner_struct

      inner struct type


      .. c:member:: int innerb

         inner member


.. c:type:: void (*sample_func_ptr)(int )

   function typedef


.. c:function:: int fxn(int a, int b)

   function declaration


.. c:var:: int eof_variable

   trailing comment at end of file

