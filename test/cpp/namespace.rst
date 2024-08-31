
.. cpp:function:: int A::B::testa(int a)

   Test fct A


.. cpp:class:: A::B::TestB

   Test cls B


   .. cpp:function:: public int testb(int b)

      Test fct B


   .. cpp:member:: private double b

      Not constant


.. cpp:var:: constexpr double CONSTANT

   Some constant


.. cpp:class:: A::TestD: public A::B::TestB

   Test cls D


   .. cpp:function:: public int testd(void) const

      Test fct D


.. cpp:function:: template<typename T> int A::testc(int c)

   Test fct C


.. cpp:enum-class:: A::TestE

   Test enum E


   .. cpp:enumerator:: A

      enum member A


   .. cpp:enumerator:: B

      enum member B


.. cpp:class:: foo::foo_class

   foo_class


   .. cpp:member:: private int m

      member


.. cpp:struct:: foo::foo_struct

   foo_struct


   .. cpp:member:: public int m

      member


.. cpp:union:: foo::foo_union

   foo_union


   .. cpp:member:: int m1

      member1


   .. cpp:member:: int m2

      member2


.. cpp:var:: const int GLOBAL

   Const.


.. cpp:enum:: foo::foo_enum

   enum


   .. cpp:enumerator:: FOO_ENUMERATOR

      enumerator

