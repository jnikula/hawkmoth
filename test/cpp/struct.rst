
.. cpp:struct:: sample_struct

   This is a sample struct

   Woohoo.


   .. cpp:member:: public int jesh

      member


   .. cpp:member:: public int array_member[5]

      array member


   .. cpp:member:: public void *pointer_member

      pointer member


   .. cpp:member:: public int (*function_pointer_member)(int, int)

      function pointer member with parameter names omitted


   .. cpp:member:: public int (*other_function_pointer_member)(int foo, int bar)

      function pointer member with parameter names

      :param foo: the foo
      :param bar: the bar


   .. cpp:member:: public struct sample_struct *next

      foo next


.. cpp:struct:: @anonymous_7bf120438d254a91e1275b973de6a0eb

   Anonymous struct documentation.


   .. cpp:member:: public int foo

      Struct member.


.. cpp:struct:: foo_struct

   Named struct.


   .. cpp:struct:: @anonymous_a63d10331be1a527625db63b8ace540f

      Anonymous sub-struct.


      .. cpp:member:: public int foo_member

         Member foo.


   .. cpp:union:: @anonymous_69382278a84175c1cbff40d522114b38

      Anonymous sub-union.


      .. cpp:member:: int bar_member_1

         Member bar 1.


      .. cpp:member:: int bar_member_2

         Member bar 2.

