all:

subdirs := test

include $(subdirs:%=%/Makefile.local)
