/**
 * Recommended formatting.
 *
 * :param foo: foo
 *   continuation with spaces
 * :param bar: bar
 *   continuation with spaces
 */
int space_star_space(int foo, int bar);

/**
No prefix at all.

:param foo: foo
  continuation with spaces
:param bar: bar
  continuation with spaces
*/
int no_prefix(int foo, int bar);

/**
    Prefix with spaces.

    :param foo: foo
      continuation with spaces
    :param bar: bar
      continuation with spaces
*/
int space_prefix(int foo, int bar);

/**
	Tab prefix.

	:param foo: foo
		continuation with tab
	:param foo: bar
		continuation with tab
*/
int tab(int foo, int bar);

/**	Tab prefix, content on first line.

	:param foo: foo
		continuation with tab
	:param foo: bar
		continuation with tab
*/
int tab_first_line_content(int foo, int bar);

/** Not recommended.
 *
 * :param foo: foo
 *   continuation with spaces
 * :param bar: bar
 *   continuation with spaces
 */
int space_star_space_first_line_content(int foo, int bar);

/**
 *Not recommended.
 *
 *:param foo: foo
 *  continuation with spaces
 *:param bar: bar
 *  continuation with spaces
 */
int space_star(int foo, int bar);

/**
No prefix, bulleted list:

* Bullet foo.
* Bullet bar.
*/
int no_prefix_star_bullets(int foo, int bar);

/**
 * Normal, bulleted list:
 *
 * * Bullet foo.
 * * Bullet bar.
 */
int space_star_space_star_bullets(int foo, int bar);

/**
 *	
 *   
 * 
 * Leading and trailing blank line removal.
 *	
 *   
 * 
 */
int blank_lines(int foo, int bar);

/** One line comment. */
int one_liner(int foo, int bar);

/** 	 One line comment with leading and trailing whitespace.  	 */
int one_liner_whitespace(int foo, int bar);

/** Two line comment.
 */
int two_liner(int foo, int bar);

/** 	 Two line comment with leading and trailing whitespace.
 	 */
int two_liner_whitespace(int foo, int bar);

