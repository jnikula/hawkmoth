# SPDX-FileCopyrightText: 2017 Jani Nikula <jani@nikula.org>
# SPDX-License-Identifier: BSD-2-Clause

# Route plain 'make' to Sphinx help
.PHONY: default
default: help

include $(shell find . -name Makefile.local)
