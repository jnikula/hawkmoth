# Copyright (c) 2016-2020 Jani Nikula <jani@nikula.org>
# Copyright (c) 2018-2020 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
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
    return comment.strip()

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
    return re.sub('(?m)^(?!$)', '   ' * nest, text)
