#
# Tests based on cmdtest(1)
#
# Deviations from standard cmdtest usage:
# - Uses .script symlinks to shared hawkmoth-wrapper.
# - Uses .c for input files.
# - Uses .stdin for additional arguments to hawkmoth.
#
# FIXME: This is *completely* inadequate. Needs to take into account compat
# options for Javadoc and check for different input. Needs more test data, in
# particular more pathological real world test data. Needs a way to flag broken
# tests for TDD. Needs to run the directive extension too, not just the comment
# extraction part.
#

HAWKMOTH:=../hawkmoth.py

# Existence of .c defines the test, not .script.
TEST:=$(wildcard *.c)
CMDTEST_CLEAN=$(TEST:%.c=%.stderr-actual) $(TEST:%.c=%.stderr-diff)	\
	$(TEST:%.c=%.stdout-actual) $(TEST:%.c=%.stdout-diff)

# Use a shared .script.
SCRIPT:=$(TEST:%.c=%.script)
%.script:
	@ln -sf hawkmoth-wrapper $@

.PHONY: check
check: $(SCRIPT)
	@cmdtest .

clean:
	@rm -f $(SCRIPT) $(CMDTEST_CLEAN)
