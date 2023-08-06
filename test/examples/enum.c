/**
 * Frobnication modes for :c:func:`frob`.
 */
enum mode {
	/**
	 * The primary frobnication mode.
	 */
	MODE_PRIMARY,
	/**
	 * The secondary frobnication mode.
	 *
	 * If the enumerator is initialized in source, its value will also be
	 * included in documentation.
	 */
	MODE_SECONDARY = 2,
};
