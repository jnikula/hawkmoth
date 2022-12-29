/** 'restrict' pointer. */
int *restrict restrict_ptr;

/** A weirder pointer. */
const int *const restrict *restrict slightly_weirder_ptr[4][2];

/** A complex pointer type that is only legal in C. */
const char* (*const *volatile *restrict legal_type_involving_function_pointer[12][3])(const char *restrict in);

/** Function with heavily qualified argument. */
int picky_function(const char *restrict not_your_avg_ptr);
