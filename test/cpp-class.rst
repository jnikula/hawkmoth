
.. cpp:class:: foo

   Classy foo.


   .. cpp:function:: foo(void)

      :cpp:class:`foo` constructor.


   .. cpp:function:: ~foo(void)

      :cpp:class:`foo` destructor.


   .. cpp:member:: int simplest

      The simplest member.


   .. cpp:var:: static int static_member

      A static member.


   .. cpp:member:: const int const_member

      A const member.


   .. cpp:member:: volatile int volatile_member

      A volatile member.


   .. cpp:var:: static const int static_const_member

      A static const member.


   .. cpp:var:: static constexpr int static_constexpr_member

      A static constexpr member.


   .. cpp:member:: mutable int mutable_member

      A mutable member.


   .. cpp:function:: public void simple_method(void)

      A simple method.


   .. cpp:function:: public constexpr void constexpr_method(void)

      A constexpr method.


   .. cpp:function:: public static void static_method(void)

      A static method.


   .. cpp:function:: private virtual void virtual_method(void)

      A virtual method.


   .. cpp:function:: private virtual void pure_method(void) = 0

      A pure virtual method.


   .. cpp:function:: private virtual void pure_const_method(void) const = 0

      A pure const virtual method.


   .. cpp:function:: protected void const_method(void) const

      A const method.


   .. cpp:function:: protected const int *method_to_const(void)

      A method to const.


   .. cpp:function:: protected const int *const_method_to_const(void) const

      A const method to const.


.. cpp:class:: bar: private foo

   A bar, classy by nature and association. Also implicitly private.


.. cpp:class:: public_bar: public foo

   A public bar.


   .. cpp:function:: private void simple_method(void) = delete

      A deleted method.


   .. cpp:function:: private virtual void pure_method(void) override

      An overridden method.


.. cpp:class:: private_bar: private foo

   A private bar.


.. cpp:class:: protected_bar: protected foo

   A protected bar.


.. cpp:class:: ecletic_bar: public public_bar, private private_bar, protected protected_bar

   An eclectic bar.


.. cpp:class:: completely_different

   And now for something...


   .. cpp:function:: completely_different(void) = default

      Something completely different.


   .. cpp:function:: private completely_different operator+(const completely_different &a)

      Operator overload.


.. cpp:class:: @anonymous_8f3f3775b6f196ec9d9cdbdbd61fc9b3

   Anonymous class.


   .. cpp:member:: int foo

      Member.

