/**
 * This is a variable document.
 */
static int sheesh;

/**
 * function pointer variable
 */
int (*function_pointer_variable)(int *param_name_ignored);

/**
 * pointer to function pointer variable
 */
int (**pointer_to_function_pointer_variable)(int);

/**
 * array of function pointers
 */
void (*function_pointer_array[5])(void);

/**
 * function pointer with lots of const qualifiers
 */
const char* (*const function_pointer_with_qualifier)(const char *in);

/**
 * Array of pointers.
 */
char *array_of_pointers[1];

/**
 * Multi-dimensional array.
 */
int multi_dim[1][2];
