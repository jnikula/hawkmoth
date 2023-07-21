
.. c:struct:: sample_struct

   This is a sample struct

   Woohoo.


   .. c:member:: int array_member[5]

      array member


   .. c:member:: int (*function_pointer_member)(int, int)

      function pointer member with parameter names omitted


   .. c:member:: int (*other_function_pointer_member)(int foo, int bar)

      function pointer member with parameter names

      :param foo: the foo
      :param bar: the bar


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

