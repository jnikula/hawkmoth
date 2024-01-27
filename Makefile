# Route plain 'make' to Sphinx help
.PHONY: default
default: help

include $(shell find -name Makefile.local)
