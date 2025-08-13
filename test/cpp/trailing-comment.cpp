
#define SAMPLE_MACRO 42              /**< macro */

#define FUNCTION_MACRO(a, b) (a + b) /**< function-like macro */

/** 
 * Documented enum
 */
enum sample_enum {
    VALUE_ONE,     /**< enumerator 1 */
    VALUE_TWO,     /**< enumerator 2 */
    VALUE_THREE    /**< enumerator 3 */
}; 

/** 
 * Documented union 
 */
union sample_union {
    int int_value;     /**< union member 1 */
    float float_value; /**< union member 2 */
}; 

/** 
 * Documented struct 
 */
struct sample_struct {
    int trailing1;    /**< struct member 1 */
    double trailing2; /**< struct member 2 */
    void* trailing3;  /**< struct member 3 */
};

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


/**
 * Documented class
 */
class sample_class {
    public:
        int member1;            /**< class member 1 */
        double member2;         /**< class member 2 */
        void* member3;          /**< class member 3 */
        int method(int a);      /**< class method */
    private:
        int private_member;     /**< private member */
};

typedef void (*sample_func_ptr)(int); /**< function typedef */

int fxn(int a, int b);                /**< function declaration */

// Exceptions

typedef struct {
    int a;
    int b; 
} multiline; /**< Multiline construct not documented */

int a;
/**< trailing comment must start on the same line as the construct */

/** This leading comment should still apply */
int b; /**< trailing comment does not merge with leading comment */

int multiline_comment; /**<
                        * trailing comment that has multiple lines
                        * should wrap correctly.
                        */

/**< trailing comment at global scope should not apply to anything */

// Check EOF handling

int tester3; /**< trailing comment at end of file */