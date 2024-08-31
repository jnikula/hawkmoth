# Copyright (c) 2016-2017, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Alternative docstring syntax
============================

This module abstracts different compatibility options converting different
syntaxes into 'native' reST ones.
"""

import re
from sphinx.util import logging

logger = logging.getLogger(__name__)
logger.warning('hawkmoth.util.doccompat module has been deprecated.')

# Basic Javadoc/Doxygen/kernel-doc import
#
# FIXME: try to preserve whitespace better

def javadoc(comment):
    """Basic javadoc conversion to reStructuredText"""

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

    return comment

def javadoc_liberal(comment):
    """Liberal javadoc conversion to reStructuredText"""

    comment = javadoc(comment)

    # Liberal conversion of any @tags, will fail for @code etc. but don't
    # care.
    comment = re.sub(r"(?m)^([ \t]*)@([a-zA-Z0-9_]+)([ \t]+)",
                     "\n\\1:\\2:\\3", comment)

    return comment

def kerneldoc(comment):
    """Basic kernel-doc conversion to reStructuredText"""

    comment = re.sub(r"(?m)^([ \t]*)@(returns?|RETURNS?):([ \t]+|$)",
                     "\n\\1:return:\\3", comment)
    comment = re.sub(r"(?m)^([ \t]*)@([a-zA-Z0-9_]+|\.\.\.):([ \t]+)",
                     "\n\\1:param \\2:\\3", comment)

    return comment

def convert(comment, **options):
    """Convert documentation from a supported syntax into reST."""

    transform = options.get('transform')

    transformations = {
        'javadoc-basic': javadoc,
        'javadoc-liberal': javadoc_liberal,
        'kernel-doc': kerneldoc,
    }

    if transform in transformations:
        comment = transformations[transform](comment)

    return comment
