/**
 * The ``c:autodoc`` directive is the easiest way to extract all the
 * documentation comments from one or more source files in one go. The
 * other directives provide more fine-grained control over what to
 * document.
 *
 * This example provides a brief overview of the most common features.
 *
 * Note that the documentation comments below are **not** good examples
 * of how to document your code. Instead, the comments primarily
 * describe the features of Hawkmoth and Sphinx.
 *
 * Source files may contain documentation comments not attached to any C
 * constructs. They will be included as generic documentation comments,
 * like this one.
 */

/**
 * Macro documentation.
 */
#define ERROR -1

/**
 * Struct documentation.
 */
struct foo {
	const char *m1; /**< Member documentation. */
	int m2;         /**< Member documentation. */
};

/**
 * Enum documentation.
 */
enum bar {
	E1, /**< Enumeration constant documentation. */
	E2, /**< Enumeration constant documentation. */
};

/**
 * Function documentation.
 *
 * :param p1: Parameter documentation
 * :param int p2: Parameter documentation with type
 * :return: Return value documentation
 */
int baz(int p1, int p2);
