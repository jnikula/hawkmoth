# Copyright (c) 2016-2017 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Documentation strings manipulation library
==========================================

This module allows a generic way of generating reST documentation for each C
construct.
"""

import re

def strip(comment):
    """Strip comment from comment markers."""
    comment = re.sub(r'^/\*\*[ \t]?', '', comment)
    comment = re.sub(r'\*/$', '', comment)
    # Could look at first line of comment, and remove the leading stuff there
    # from the rest.
    comment = re.sub(r'(?m)^[ \t]*\*?[ \t]?', '', comment)
    # Strip leading blank lines.
    comment = re.sub(r'^[\n]*', '', comment)
    # End in exactly one newline.
    comment = re.sub(r'[\n]*$', '', comment) + '\n'
    return comment

def wrap_blank_lines(string):
    return '\n' + string + '\n'

def is_doc(comment):
    """Test if comment is a C documentation comment."""
    return comment.startswith('/**') and comment != '/**/'

def nest(text, nest):
    """
    Indent documentation block for nesting.

    Args:
        text (str): Documentation body.
        nest (int): Nesting level. For each level, the final block is indented
            one level. Useful for (e.g.) declaring structure members.

    Returns:
        str: Indented reST documentation string.
    """
    return re.sub('(?m)^', '   ' * nest, text)
