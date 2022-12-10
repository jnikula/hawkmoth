/**
 * Compat comment transformations.
 *
 * Transformations require ``cautodoc_transformations`` configuration in
 * ``conf.py``. In this example, a transformation is used to support
 * Javadoc-style documentation comments.
 *
 * @param list The list to frob.
 * @param mode The frobnication mode.
 * @return 0 on success, non-zero error code on error.
 * @since v0.1
 */
int frob2(struct list *list, enum mode mode);
