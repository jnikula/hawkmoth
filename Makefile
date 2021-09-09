all:

subdirs := . test doc hawkmoth docker

include $(subdirs:%=%/Makefile.local)
include Makefile.rules
