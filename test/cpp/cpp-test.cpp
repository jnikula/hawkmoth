/** This is a top level comment from the code. */

/** Macro. */
#define FOO

/** Function like macro. */
#define FOOING(x) x

/**
 * Function.
 *
 * :param bar: Some parameter.
 * :param baz: Some other parameter.
 *
 * A link to a struct documentation from the code :cpp:any:`stfoo`.
 */
int foo(int bar, int baz);

/** Variable. */
int fooer;

/** Struct. */
struct stfoo {
	/** Member. */
	int foo;
};

/** Enum. */
enum somefoos {
	/** one */
	FOO1,
	/** two */
	FOO2,
	/** three */
	FOO3,
};

/** Anonymous structure. */
struct {
	/** Anonymous sub-struct. */
	struct {
		/** Member foo. */
		int foo_member;
	} foo;

	/** Anonymous sub-union. */
	union {
		/** Member bar 1. */
		int bar_member_1;
		/** Member bar 2. */
		int bar_member_2;
	} bar;
} alt_stfoo_var;

/** Membering. */
int (*foopointer)(int, int);

/** Memberings. */
int (*foopointers[5])(int, int);

/** Union. */
union foonion {

	/** Member. */
	int foo;

	/** Member. */
	int bar;

	/** Member member. */
	struct stfoo member_berry;

	/** Membering. */
	int (*foomember)(int, int);

	/** Memberings. */
	int (*foomembers[5])(int, int);
};
