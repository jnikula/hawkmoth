all:

subdirs := test

include $(subdirs:%=%/Makefile.local)
include Makefile.rules
