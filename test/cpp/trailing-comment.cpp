//////////////////////////
// Macro permutations
//////////////////////////

#define SAMPLE_MACRO 42 ///< macro with trailing comment
#define FUNCTION_MACRO(a, b) (a + b) ///< function-like macro with trailing comment

#define MULTILINE_MACRO(a, b) \
    do { \
        a += b; \
        b += a; \
    } while (0) ///< multiline macro with trailing comment

//////////////////////////
// Check trailing comment markers inside leading comments
//////////////////////////

/** leading comment with a trailing comment marker ///< should not be treated as a trailing comment */
int leading_comment_with_trailing_marker;

/**
///< trailing comment marker at beginning of line
 */
int leading_comment_with_trailing_marker2;

//////////////////////////
// Apply trailing comments to the underlying enum/struct/union, not the typedef
//////////////////////////

typedef enum {
    VALUE_ONE, ///< enum value with trailing comment
    VALUE_TWO, ///< another enum value with trailing comment
    VALUE_THREE ///< yet another enum value with trailing comment
} sample_enum; ///< enum trailing comment for c style enum

enum sample_enum2 {
    VALUE_FOUR, ///< another enum value with trailing comment
    VALUE_FIVE ///< yet another enum value with trailing comment
}; ///< trailing comment for c++ style enum

enum class sample_enum3 {
    VALUE_SIX, ///< enum class value with trailing comment
    VALUE_SEVEN ///< another enum class value with trailing comment
}; ///< trailing comment for c++ enum class


typedef union {
    int int_value; ///< union member with trailing comment
    float float_value; ///< another union member with trailing comment
} sample_union; ///< union trailing comment

union sample_union2 {
    int int_value2; ///< union member with trailing comment
    double double_value; ///< another union member with trailing comment
}; ///< trailing comment for c++ style union


typedef struct  {
    int trailing1; ///< trailing comment for member
    double trailing2; ///< trailing comment only
    void* trailing3; ///< trailing comment
} sample_struct; ///< trailing comment for struct

struct sample_struct2 {
    int trailing1; ///< trailing comment for member
    double trailing2; ///< trailing comment only
    void* trailing3; ///< trailing comment
}; ///< trailing comment for c++ style struct


class SampleClass { ///< class with trailing comment
public:
    int member1; ///< class member with trailing comment
    double member2; ///< another class member with trailing comment

    struct InnerStruct {
        int inner_member; ///< inner struct member with trailing comment
    } inner; ///< trailing comment for inner struct member

    struct InnerStructType {
        int inner_member2; ///< inner struct member with trailing comment
    }; ///< trailing comment for nested struct type
private:
    void private_function(); ///< private helper function with trailing comment
    int private_variable; ///< private variable with trailing comment
};

//////////////////////////
// Typedefs (no special handling needed)
//////////////////////////

typedef void (*sample_func_ptr)(int); ///< typedef with trailing comment

using sample_func_ptr_alias = sample_func_ptr; ///< using alias with trailing comment

//////////////////////////
// Handle different locations inside function definitions
//////////////////////////

int sample_func(int a, int b) ///< function with trailing comment after line
{
    return a + b;
}

int sample_func2(int a, int b)
{
    return a + b;
} ///< function with trailing comment after block

int sample_func3( ///< function with trailing comment before parameters
    int a, 
    int b
)
{
    return a + b;
}

int sample_func4(int a, int b); ///< function declaration with trailing comment

//////////////////////////
// Clear the trailing comment context correctly
//////////////////////////

int tester; ///< trailing comment 1

/** This leading comment should still apply */
int tester2; // This should clear the trailing comment context
///< this comment is ignored since it applies to the global scope and trailing comments don't work at global scope

//////////////////////////
// Check EOF handling
//////////////////////////

int tester3; ///< trailing comment at end of file
