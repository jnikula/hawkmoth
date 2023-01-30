#include <stdbool.h>

/**
 * Linked list node.
 */
struct list {
	/** Next node. */
	struct list *next;

	/** Data. */
	int data;

	/** Bool. */
	bool x;
};
