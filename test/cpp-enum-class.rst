
.. cpp:enum-class:: breakfast

   Enum class.


   .. cpp:enumerator:: spam

      Spam.


   .. cpp:enumerator:: more_spam

      More spam.


   .. cpp:enumerator:: eggs

      Eggs.


   .. cpp:enumerator:: also_spam

      Also spam.


.. cpp:enum-class:: lunch: long

   Enum struct is the same as enum class and it's all the same for referencing
   too. See: :cpp:enum:`breakfast` and :cpp:enum:`lunch`.


   .. cpp:enumerator:: much_spam

      Much spam.


   .. cpp:enumerator:: no_eggs

      No eggs.


.. cpp:enum-class:: dinner: std::underlying_type<lunch>::type

   I chose a theme and I'm sticking to it.


   .. cpp:enumerator:: only_spam

      Only spam.

