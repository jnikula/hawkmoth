# Copyright (c) 2016-2017, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Alternative docstring syntax
============================

This module abstracts different compatibility options converting different
syntaxes into 'native' reST ones.
"""

import re

# Basic Javadoc/Doxygen/kernel-doc import
#
# FIXME: One of the design goals of Hawkmoth is to keep things simple. There's a
# fine balance between sticking to that goal and adding compat code to
# facilitate any kind of migration to Hawkmoth. The compat code could be turned
# into a fairly simple plugin architecture, with some basic compat builtins, and
# the users could still extend the compat features to fit their specific needs.
def convert(comment, mode):
    """Convert documentation from a supported syntax into reST."""
    # FIXME: try to preserve whitespace better

    if mode == 'javadoc-basic' or mode == 'javadoc-liberal':
        # @param
        comment = re.sub(r"(?m)^([ \t]*)@param([ \t]+)([a-zA-Z0-9_]+|\.\.\.)([ \t]+)",
                         "\n\\1:param\\2\\3:\\4", comment)
        # @param[direction]
        comment = re.sub(r"(?m)^([ \t]*)@param\[([^]]*)\]([ \t]+)([a-zA-Z0-9_]+|\.\.\.)([ \t]+)",
                         "\n\\1:param\\3\\4: *(\\2)* \\5", comment)
        # @return
        comment = re.sub(r"(?m)^([ \t]*)@returns?([ \t]+|$)",
                         "\n\\1:return:\\2", comment)
        # @code/@endcode blocks. Works if the code is indented.
        comment = re.sub(r"(?m)^([ \t]*)@code([ \t]+|$)",
                         "\n::\n", comment)
        comment = re.sub(r"(?m)^([ \t]*)@endcode([ \t]+|$)",
                         "\n", comment)
        # Ignore @brief.
        comment = re.sub(r"(?m)^([ \t]*)@brief[ \t]+", "\n\\1", comment)

        # Ignore groups
        comment = re.sub(r"(?m)^([ \t]*)@(defgroup|addtogroup)[ \t]+[a-zA-Z0-9_]+[ \t]*",
                         "\n\\1", comment)
        comment = re.sub(r"(?m)^([ \t]*)@(ingroup|{|}).*", "\n", comment)

    if mode == 'javadoc-liberal':
        # Liberal conversion of any @tags, will fail for @code etc. but don't
        # care.
        comment = re.sub(r"(?m)^([ \t]*)@([a-zA-Z0-9_]+)([ \t]+)",
                         "\n\\1:\\2:\\3", comment)

    if mode == 'kernel-doc':
        # Basic kernel-doc convert, will document struct members as params, etc.
        comment = re.sub(r"(?m)^([ \t]*)@(returns?|RETURNS?):([ \t]+|$)",
                         "\n\\1:return:\\3", comment)
        comment = re.sub(r"(?m)^([ \t]*)@([a-zA-Z0-9_]+|\.\.\.):([ \t]+)",
                         "\n\\1:param \\2:\\3", comment)

    return comment
