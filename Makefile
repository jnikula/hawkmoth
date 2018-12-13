all:

subdirs := . test doc hawkmoth

include $(subdirs:%=%/Makefile.local)
include Makefile.rules
