
.. c:struct:: sample_struct

   This is a sample struct

   Woohoo.


   .. c:member:: int jesh

      member


   .. c:member:: int array_member[5]

      array member


   .. c:member:: void *pointer_member

      pointer member


   .. c:member:: int (*function_pointer_member)(int, int)

      function pointer member with parameter names omitted


   .. c:member:: int (*other_function_pointer_member)(int foo, int bar)

      function pointer member with parameter names

      :param foo: the foo
      :param bar: the bar


   .. c:member:: struct sample_struct *next

      foo next


.. c:struct:: @anonymous_7bf120438d254a91e1275b973de6a0eb

   Anonymous struct documentation.


   .. c:member:: int foo

      Struct member.


.. c:struct:: foo_struct

   Named struct.


   .. c:struct:: @anonymous_a63d10331be1a527625db63b8ace540f

      Anonymous sub-struct.


      .. c:member:: int foo_member

         Member foo.


   .. c:union:: @anonymous_69382278a84175c1cbff40d522114b38

      Anonymous sub-union.


      .. c:member:: int bar_member_1

         Member bar 1.


      .. c:member:: int bar_member_2

         Member bar 2.

