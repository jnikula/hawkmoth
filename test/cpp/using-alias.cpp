/** Type alias */
using footypealias = int;

/** Function alias */
using foofctalias = void(int, int);

/** Template alias */
template<typename T>
using footmplalias = T*;

/** Variadic template alias */
template<typename... Args>
using foovaralias = void(footypealias, Args...);

/** Nested template alias */
template<typename T, typename... Args>
using foonestalias = foovaralias<footmplalias<T>, Args...>;
