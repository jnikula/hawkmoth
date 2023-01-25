
.. cpp:class:: template<typename T, class C, char V> foo: private C

   Templated class.


   .. cpp:member:: private T member

      M for Member.


   .. cpp:member:: private char variable

      V for Variable.


.. cpp:class:: template<auto...> variadic_foo

   Variadic templates, why not?


.. cpp:function:: template<typename T, typename... Ts> void variadic_fooer(T foo, Ts... bar)

   A different kind of variadic template.


.. cpp:function:: template<typename T, typename... Ts> void space_fuzer(T foo, Ts... bar)

   White space shenanigans.


.. cpp:class:: template<template<typename T, class C, char V> class who> inception_foo

   Templated templated class. Puny compilers / standards don't allow further
   recursion.


   .. cpp:member:: private std::vector<int> nothing_much

      Fully defined templated type.


   .. cpp:member:: private who<int, std::vector<char>, 'z'> whoever

      Who as in 'who thought this was a good idea?'


   .. cpp:function:: private template<typename Z, typename Y> Z templated_method(Y y)

      Templated method within a template.

      :param y: Yes, this works too.


.. cpp:class:: template<template<class T, typename C, char V> typename who> alt_inception_foo

   `typename` and `class` are interchangeable, but we respect the source code
   just in case.

