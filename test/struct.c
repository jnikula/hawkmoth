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
