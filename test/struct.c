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
	 * array member
	 */
	int array_member[5];
	/**
	 * pointer member
	 */
	void *pointer_member;
	/**
	 * function pointer member
	 */
	int (*function_pointer_member)(int, int);
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
