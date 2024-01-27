# Route plain 'make' to Sphinx help
.PHONY: all
all: help

include $(shell find -name Makefile.local)
