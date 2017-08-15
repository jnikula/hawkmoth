/**
 * This file showcases the documentation comments.
 */

/**
 * True.
 */
#define TRUE 1

/**
 * Typedef documentation.
 */
typedef void * list_data_t;

/**
 * Linked list node.
 */
struct list {
	/** Next node. */
	struct list *next;

	/** Data. */
	list_data_t data;
};

/**
 * Modes.
 */
enum mode {
	/**
	 * This is the first mode.
	 */
	MODE_ONE,
	/**
	 * This is the second mode.
	 */
	MODE_TWO,
};

/**
 * List frobnicator.
 *
 * :param list: The list to frob.
 * :param mode: The frobnication mode.
 * :return: 0 on success, non-zero error code on error.
 * :since: v0.1
 */
int frob(struct list *list, enum mode mode);

/**
 * List frobnicator.
 *
 * @param list The list to frob.
 * @param mode The frobnication mode.
 * @return 0 on success, non-zero error code on error.
 * @since v0.1
 */
int frob2(struct list *list, enum mode mode);

/**
 * Frobnicate list in mode one.
 */
#define frobfrob(l) frob(l, MODE_ONE)
