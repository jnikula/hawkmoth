/**
 * Typedef documentation.
 */
typedef void * list_data_t;

/**
 * Function pointer typedef documentation.
 *
 * :param context: Context
 * :param name: Name
 * :return: 0 on success
 */
typedef int (*callback_t)(void *context, const char *name);
