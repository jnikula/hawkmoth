typedef struct {
    int a;
    int b; 
} multiline; /**< Multiline construct not documented */

int a;
/**< trailing comment must start on the same line as the construct */

/** This leading comment should still apply */
int b; /**< trailing comment does not merge with leading comment */
