#include <type_traits>

/** Enum class. */
enum class breakfast {
	/** Spam. */
	spam,

	/** More spam. */
	more_spam,

	/** Eggs. */
	eggs,

	/** Also spam. */
	also_spam,
};

/**
 * Enum struct is the same as enum class and it's all the same for referencing
 * too. See: :cpp:enum:`breakfast` and :cpp:enum:`lunch`.
 */
enum struct lunch: long {
	/** Much spam. */
	much_spam,

	/** No eggs. */
	no_eggs,
};

/** I chose a theme and I'm sticking to it. */
enum class dinner : std::underlying_type< lunch>::type {
	/** Only spam. */
	only_spam,
};
