namespace A {
	namespace B {

		/**
		 * Test fct A
		 */
		int testa(int a) { return a; }

		/**
		 * Test cls B
		 */
		class TestB {
		public:
			/**
			 * Test fct B
			 */
			int testb(int b) { return b; }

		private:
			/** Not constant */
			double b;
		};


		/** Some constant */
		constexpr double CONSTANT = 5.;

	} // namespace B

	/**
	 * Test cls D
	 */
	class TestD : public B::TestB {
	public:
		/**
		 * Test fct D
		 */
		int testd() const { return d; }
	private:
		static double d;
	};

	/**
	 * Test fct C
	 */
	template<typename T>
	int testc(int c) { return c; }

	/**
	 * Test enum E
	 */
	enum class TestE {
		/** enum member A */
		A,
		/** enum member B */
		B,
	};

} // namespace A


namespace foo {
	/**
	 * foo_class
	 */
	class foo_class {
		/** member */
		int m;
	};

	/**
	 * foo_struct
	 */
	struct foo_struct {
		/** member */
		int m;
	};

	/**
	 * foo_union
	 */
	union foo_union {
		/** member1 */
		int m1;
		/** member2 */
		int m2;
	};

	/**
	 * Const.
	 */
	const int GLOBAL = 5;

	/** enum */
	enum foo_enum {
		/** enumerator */
		FOO_ENUMERATOR,
	};
};
