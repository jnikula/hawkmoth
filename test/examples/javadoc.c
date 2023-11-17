struct list;
enum mode;

/**
 * Custom comment transformations.
 *
 * Documentation comments can be processed using the hawkmoth-process-docstring
 * Sphinx event. You can use the built-in extensions for this, or create your
 * own.
 *
 * In this example, <tt>hawkmoth.ext.javadoc</tt> built-in extension is used to
 * support Javadoc/Doxygen-style documentation comments. You can use both \@ and
 * \\ for the commands.
 *
 * \note
 * While the most common commands and inline markup \a should work, the
 * Javadoc/Doxygen support is nowhere near complete.
 *
 * The support should be good enough for basic API documentation, including
 * things like code blocks:
 *
 * \code
 * ¯\_(ツ)_/¯
 * \endcode
 *
 * And parameter and return value descriptions, and the like:
 *
 * @param list The list to frob.
 * @param[in] mode The frobnication mode.
 * @return 0 on success, non-zero error code on error.
 * @since v0.1
 */
int frob2(struct list *list, enum mode mode);
