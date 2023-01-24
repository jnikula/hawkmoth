/**
 * Custom comment transformations.
 *
 * Documentation comments can be processed using the hawkmoth-process-docstring
 * Sphinx event. You can use the built-in extensions for this, or create your
 * own.
 *
 * In this example, hawkmoth.ext.napoleon built-in extension is used to support
 * Napoleon-style documentation comments.
 *
 * Args:
 *     foo: This is foo.
 *     bar: This is bar.
 *
 * Return:
 *     Status.
 */
int napoleon(int foo, char *bar);
