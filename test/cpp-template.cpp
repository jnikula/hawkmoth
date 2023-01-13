#include <vector>

/** Templated class. */
template <typename T, class C, char V>
class foo: C {
	/** M for Member. */
	T member;

	/** V for Variable. */
	char variable = V;
};

/** Variadic templates, why not? */
template<auto...>
class variadic_foo;

/** A different kind of variadic template. */
template<typename T, typename... Ts>
void variadic_fooer(T foo, Ts ... bar);

/** White space shenanigans. */
template < typename T ,typename ...Ts>
void space_fuzer(T foo,Ts ... bar);

/**
 * Templated templated class. Puny compilers / standards don't allow further
 * recursion.
 */
template<template<typename T, class C, char V> class who>
class inception_foo {

	/** Fully defined templated type. */
	std::vector<int> nothing_much;

	/** Who as in 'who thought this was a good idea?' */
	who<int, std::vector<char>, 'z'> whoever;

	/**
	 * Templated method within a template.
	 *
	 * :param y: Yes, this works too.
	 */
	template<typename Z, typename Y> Z templated_method(Y y);
};

/**
 * `typename` and `class` are interchangeable, but we respect the source code
 * just in case.
 */
template<template<class T, typename C, char V> typename who>
class alt_inception_foo;
