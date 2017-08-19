all:

subdirs := test doc

include $(subdirs:%=%/Makefile.local)
include Makefile.rules
