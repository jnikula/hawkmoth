#define MACRO_SIZE 12

enum {
	ENUM_SIZE = 4,
	ENUM_MAX,
};

/**
 * array
 */
static int foo[MACRO_SIZE];

/**
 * array
 */
static int bar[MACRO_SIZE*ENUM_SIZE][3];

/**
 * function
 */
int array(int foo[MACRO_SIZE/ENUM_SIZE]);

/**
 * structure
 */
struct s {
	/** member */
	long m[ENUM_MAX];
};
