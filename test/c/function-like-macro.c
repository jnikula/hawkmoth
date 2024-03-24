/**
 * A function-like macro.
 */
#define FOO(bar, baz) (bar)

/**
 * Another
 */
#define BAR() yeah

/**
 * Standard vararg.
 */
#define VARARG0(...) __VA_ARGS__

/**
 * Named argument and standard varargs.
 */
#define VARARG1(par0, ...) __VA_ARGS__

/**
 * Named varargs.
 */
#define VARARG0_NAMED(named...) named

/**
 * Named argument and named varargs.
 */
#define VARARG1_NAMED(par0, named...) named
