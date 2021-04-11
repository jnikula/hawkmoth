/**
 * Custom comment transformations.
 *
 * Transformations require ``cautodoc_transformations`` configuration in
 * ``conf.py``. In this example, Napoleon is used to interpret another
 * documentation comment format.
 *
 * Args:
 *     foo: This is foo.
 *     bar: This is bar.
 *
 * Return:
 *     Status.
 */
int napoleon(int foo, char *bar);
