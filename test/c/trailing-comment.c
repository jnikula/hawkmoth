
#define SAMPLE_MACRO 42              /**< macro */

#define FUNCTION_MACRO(a, b) (a + b) /**< function-like macro */

/** 
 * Documented enum
 */
typedef enum {
    VALUE_ONE,         /**< enumerator 1 */
    VALUE_TWO = 1,     /**< enumerator 2 */
    VALUE_THREE = 2    /**< enumerator 3 */
} sample_enum; 

/** 
 * Documented union 
 */
typedef union {
    int int_value;     /**< union member 1 */
    float float_value; /**< union member 2 */
} sample_union; 

/** 
 * Documented struct 
 */
typedef struct  {
    int trailing1;    /**< struct member 1 */
    double trailing2; /**< struct member 2 */
    void* trailing3;  /**< struct member 3 */
} sample_struct;

/**
 * Documented compound struct
 */
struct outer_struct {

    int outer;                   /**< outer member */

    /** inner struct type */
    struct inner_struct {
        int innera;
        int innerb;              /**< inner member */
    } a;
};

typedef void (*sample_func_ptr)(int); /**< function typedef */

int fxn(int a, int b);                /**< function declaration */

int eof_variable; /**< trailing comment at end of file */