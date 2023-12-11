
.. cpp:type:: footypealias = int

   Type alias


.. cpp:type:: foofctalias = void (int, int)

   Function alias


.. cpp:type:: template<typename T> footmplalias = T *

   Template alias


.. cpp:type:: template<typename... Args> foovaralias = void (footypealias, Args...)

   Variadic template alias


.. cpp:type:: template<typename T, typename... Args> foonestalias = foovaralias<footmplalias<T>, Args...>

   Nested template alias

