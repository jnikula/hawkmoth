#
# Dead simple test framework.
#
# Add a .c file with documentation comments, and an accompanying .expect file
# with the expected extracted documentation.
#
# FIXME: This is *completely* inadequate. Needs to take into account compat
# options for Javadoc and check for different input. Needs more test data, in
# particular more pathological real world test data. Needs a way to flag broken
# tests for TDD. Needs a way to handle stderr and exit code. Needs to run the
# directive extension too, not just the comment extraction part.
#

HAWKMOTH:=../hawkmoth.py

EXPECT:=$(wildcard *.expect)
OUTPUT:=$(EXPECT:%.expect=%.output)
DIFF:=$(EXPECT:%.expect=%.diff)

.PRECIOUS: %.output
%.output: %.c $(HAWKMOTH)
	@$(HAWKMOTH) $< > $@

%.diff: %.expect %.output
	@diff -u $^ > $@ || true

.PHONY: check
check: $(DIFF)
	@cat $(DIFF)

clean:
	@rm -f $(OUTPUT) $(DIFF)
