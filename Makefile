# Route plain 'make' to Sphinx help
.PHONY: all
all: help

subdirs := . test doc src/hawkmoth docker

include $(subdirs:%=%/Makefile.local)
