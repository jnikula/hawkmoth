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

def _strip(comment):
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

def generate(text, indent, fmt, name=None,
             ttype=None, args=None, transform=None):
    """
    Generate reST documentation string.

    Args:
        text (str): Documentation body.
        fmt (enum :py:class:`Type`): Format type to use. Different formats
            require different arguments and ignores others if given.
        name (str): Name of the documented token.
        ttype (str): Type of the documented token.
        args (list): List of arguments (str).
        transform (func): Transformation function to be applied to the
            documentation body. This is useful (e.g.) to extend the generator
            with different syntaxes by converting them to reST. This is applied
            on the documentation body after removing comment markers.

    Returns:
        str: reST documentation string.
    """

    text = _strip(text)

    if transform is not None:
        text = transform(text)

    if args is not None:
        args = ', '.join(args)

    text = nest(text, indent)
    return fmt.format(text=text, name=name, ttype=ttype, args=args)
