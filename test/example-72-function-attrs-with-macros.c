#define EXPORT_DEFAULT __attribute__ ((visibility("default")))
#define EXPORT_HIDEN __attribute__ ((visibility("hidden")))

/**
 * List frobnicator with visibility hidden attribute.
 *
 * :param list: The list to frob.
 * :param mode: The frobnication mode.
 * :return: 0 on success, non-zero error code on error.
 * :since: v0.1
 */
EXPORT_HIDEN
int hidden_frob(struct list *list, enum mode mode);

/**
 * List frobnicator with visibility default attribute.
 *
 * :param list: The list to frob.
 * :param mode: The frobnication mode.
 * :return: 0 on success, non-zero error code on error.
 * :since: v0.1
 */
EXPORT_DEFAULT
int default_frob(struct list *list, enum mode mode);
