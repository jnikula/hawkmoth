
.. c:struct:: sample_struct

   This is a sample struct

   Woohoo.


   .. c:member:: int jesh

      member


   .. c:member:: bool bool_member

      bool member


   .. c:member:: bool _Bool_member

      _Bool member


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


.. c:struct:: @anonymous_a6168a23d6840e8919ade5661a307607

   Anonymous struct documentation.


   .. c:member:: int foo

      Struct member.


.. c:struct:: foo_struct

   Named struct.


   .. c:struct:: @anonymous_0a4d6f0b47cde0e9872b6dbde2ad1c1a

      Anonymous sub-struct.


      .. c:member:: int foo_member

         Member foo.


   .. c:union:: @anonymous_22cf17aa0fa6d83246282a58013db249

      Anonymous sub-union.


      .. c:member:: int bar_member_1

         Member bar 1.


      .. c:member:: int bar_member_2

         Member bar 2.

