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
                        * should not be applied
                        */

void short_function(void) /**< no comments in middle of line */ {return;}

void short_function_2( /**< no comments in middle of construct */ void) {return;}
