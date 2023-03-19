/**
 * Circle.
 */
class Circle {
private:
	/** Radius */
	int radius;

public:
	/** Constructor */
	Circle(int radius);

	/** Destructor */
	~Circle();

	/** Get the area. */
	virtual int area(void);
};
