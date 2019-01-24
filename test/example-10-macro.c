/**
 * Failure status.
 */
#define FAILURE 13

/**
 * Terminate immediately with failure status.
 *
 * See :c:macro:`FAILURE`.
 */
#define DIE() _exit(FAILURE)

/**
 * Get the number of elements in an array.
 *
 * :param array: An array
 * :return: Array size
 */
#define ARRAY_SIZE(array) (sizeof(array) / sizeof(array[0]))

/**
 * Variadic macros
 *
 * :param foo: regular argument
 * :param ...: variable argument
 */
#define VARIADIC_MACRO(foo, ...) (__VA_ARGS__)
