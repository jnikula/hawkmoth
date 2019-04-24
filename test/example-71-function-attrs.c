/**
 * List frobnicator with pure attribute.
 *
 * :param list: The list to frob.
 * :param mode: The frobnication mode.
 * :return: 0 on success, non-zero error code on error.
 * :since: v0.1
 */
__attribute__((pure))
int pure_frob(struct list *list, enum mode mode);

/**
 * List frobnicator with const attribute
 *
 * :param list: The list to frob.
 * :param mode: The frobnication mode.
 * :return: 0 on success, non-zero error code on error.
 * :since: v0.1
 */
__attribute__((const))
int const_frob(struct list *list, enum mode mode);
