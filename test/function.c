/**
 * Foo function.
 */
int foo(int bar, int baz);

/**
 * No parameters.
 */
int no_parameters(void);

/**
 * Empty parameter list.
 */
int empty_parameter_list();

/**
 * Variadic function.
 */
int variadic(const char *fmt, ...);

/**
 * Array parameters.
 */
void foorray(const double array[], int x[5]);

/**
 * Array parameters with multiple dimensions.
 *
 * Clang removes spaces.
 */
void multi_array_param(int x[2][2], int y [2] [2]);

/**
 * Function pointer parameter.
 */
void function_pointer_param(void* (*hook)(void *p, int n));

/**
 * Array of pointers parameter.
 */
void array_of_pointer_params(char *p[]);
