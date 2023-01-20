/**
 * Classy foo.
 */
class foo {
public:
	/** :cpp:class:`foo` constructor. */
	foo();

	/** :cpp:class:`foo` destructor. */
	~foo();

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

	/** A mutable member. */
	mutable int mutable_member;

	/** A simple method that will not throw. */
	void simple_method(void) noexcept;

	/** A constexpr method. */
	constexpr void constexpr_method(void);

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

/** A bar, classy by nature and association. Also implicitly private. */
class bar: foo {
};

/** A public bar. */
class public_bar: public foo {
	/** A deleted method. */
	void simple_method(void) = delete;

	/** An overridden method. */
	void pure_method(void) override;
};

/** A private bar. */
class private_bar: private foo {
};

/** A protected bar. */
class protected_bar: protected foo {
};

/** An eclectic bar. */
class ecletic_bar: public public_bar, private private_bar, protected protected_bar {
};

/** And now for something... */
class completely_different {
	/** Something completely different. */
	completely_different() = default;

	/** Operator overload. */
	completely_different operator+ (const completely_different &a);
};

/** Anonymous class. */
class {
	/** Member. */
	int foo;
} C;
