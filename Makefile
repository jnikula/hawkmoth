all:

subdirs := . test doc src/hawkmoth docker

include $(subdirs:%=%/Makefile.local)
include Makefile.rules
