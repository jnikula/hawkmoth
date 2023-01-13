
.. cpp:struct:: all_is_class

   C++ structures are classes with different default access specifiers.


   .. cpp:function:: all_is_class(void)

      Struct constructor.


   .. cpp:function:: ~all_is_class(void)

      Struct destructor.


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


   .. cpp:function:: public void simple_method(void)

      A simple method.


   .. cpp:function:: public void simple_method_2(void)

      Another simple method.


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


.. cpp:struct:: just_in_case: public all_is_class

   C++ structures are classes with different default access specifiers.

