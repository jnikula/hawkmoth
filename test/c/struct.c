#include <stdbool.h>

/**
 * This is a sample struct
 *
 * Woohoo.
 */
struct sample_struct {
	/**
	 * member
	 */
	int jesh;
	/**
	 * bool member
	 */
	bool bool_member;
	/**
	 * _Bool member
	 */
	_Bool _Bool_member;
	/**
	 * array member
	 */
	int array_member[5];
	/**
	 * pointer member
	 */
	void *pointer_member;
	/**
	 * function pointer member with parameter names omitted
	 */
	int (*function_pointer_member)(int, int);
	/**
	 * function pointer member with parameter names
	 *
	 * :param foo: the foo
	 * :param bar: the bar
	 */
	int (*other_function_pointer_member)(int foo, int bar);
	/**
	 * foo next
	 */
	struct sample_struct *next;
};

/**
 * Anonymous struct documentation.
 */
struct {
	/**
	 * Struct member.
	 */
	int foo;
} variable;

/**
 * Named struct.
 */
struct foo_struct {
	/**
	 * Anonymous sub-struct.
	 */
	struct {
		/**
		 * Member foo.
		 */
		int foo_member;
	} foo;
	/**
	 * Anonymous sub-union.
	 */
	union {
		/**
		 * Member bar 1.
		 */
		int bar_member_1;
		/**
		 * Member bar 2.
		 */
		int bar_member_2;
	} bar;
};
