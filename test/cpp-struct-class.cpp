/** C++ structures are classes with different default access specifiers. */
struct all_is_class {
	/** Struct constructor. */
	all_is_class();

	/** Struct destructor. */
	~all_is_class();

public:
	/** The simplest member. */
	int simplest;

	/** A static member. */
	static int static_member;

	/** A const member. */
	const int const_member;

	/** A volatile member. */
	volatile int volatile_member;

	/** A static const member. */
	static const int static_const_member;

	/** A static constexpr member. */
	static constexpr int static_constexpr_member = 0;

	/** A simple method. */
	void simple_method(void);

	/** Another simple method. */
	void simple_method_2(void);

	/** A static method. */
	static void static_method(void);

private:
	/** A virtual method. */
	virtual void virtual_method(void);

	/** A pure virtual method. */
	virtual void pure_method(void) = 0;

	/** A pure const virtual method. */
	virtual void pure_const_method(void) const = 0;

protected:
	/** A const method. */
	void const_method(void) const;

	/** A method to const. */
	const int *method_to_const(void);

	/** A const method to const. */
	const int *const_method_to_const(void) const;
};

/** C++ structures are classes with different default access specifiers. */
struct just_in_case: all_is_class {
};
