#include <stdbool.h>

/**
 * Retain bool instead of using _Bool.
 */
static bool convert_bool;

/**
 * Also convert _Bool to bool.
 */
static _Bool convert_Bool;

/**
 * Bool function.
 */
bool boolean(bool bar, _Bool baz);

/**
 * This is a sample struct
 *
 * Woohoo.
 */
struct sample_struct {
	/**
	 * bool member
	 */
	bool bool_member;
	/**
	 * _Bool member
	 */
	_Bool _Bool_member;
};
