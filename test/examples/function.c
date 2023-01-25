struct list;
enum mode;

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
 * variadic frobnicator
 *
 * :param fmt: the format
 * :param ...: variadic
 */
int frobo(const char *fmt, ...);
