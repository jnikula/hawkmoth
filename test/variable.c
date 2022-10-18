/**
 * This is a variable document.
 */
static int sheesh;

/**
 * function pointer variable
 */
int (*function_pointer_variable)(int *param_name_ignored);

/**
 * variadic function pointer variable
 */
int (*variadic_function_pointer_variable)(int *param_name_ignored, ...);

/**
 * pointer to function pointer variable
 */
int (**pointer_to_function_pointer_variable)(int);

/**
 * array of function pointers
 */
void (*function_pointer_array[5])(void);

/**
 * array of array of function pointers
 */
void (*array_of_function_pointer_array[5][15])(void);

/**
 * function pointer with lots of const qualifiers
 */
const char* (*const function_pointer_with_qualifier)(const char *in);

/**
 * function pointer with multiple qualifiers
 */
const char* (*const volatile function_pointer_with_multiple_qualifiers)(const char *in);

/**
 * a complex type involving function pointers somehow
 */
const char* (*const *volatile *restrict legal_type_involving_function_pointer[12][3])(const char *in);

/**
 * function pointer to a function taking a function pointer as arg
 */
int (*function_pointer_with_function_pointer_arg)(float (*arg1)(char c));

/**
 * Array of pointers.
 */
char *array_of_pointers[1];

/**
 * Multi-dimensional array.
 */
int multi_dim[1][2];
