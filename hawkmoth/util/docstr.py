# Copyright (c) 2016-2017 Jani Nikula <jani@nikula.org>
# Copyright (c) 2018-2019 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Documentation strings manipulation library
==========================================

This module allows a generic way of generating reST documentation for each C
construct.
"""

import re
from enum import Enum, auto

class Type(Enum):
    """Enumeration of supported formats."""
    TEXT = auto()
    VAR = auto()
    TYPE = auto()
    ENUM_VAL = auto()
    MEMBER = auto()
    MACRO = auto()
    MACRO_FUNC = auto()
    FUNC = auto()

# Dictionary of tuples (text indentation level, format string).
#
# Text indentation is required for indenting the documentation body relative to
# directive lines.
_doc_fmt = {
    Type.TEXT:       (0, '\n{text}\n'),
    Type.VAR:        (1, '\n.. c:var:: {ttype} {name}\n\n{text}\n'),
    Type.TYPE:       (1, '\n.. c:type:: {name}\n\n{text}\n'),
    Type.ENUM_VAL:   (1, '\n.. c:macro:: {name}\n\n{text}\n'),
    Type.MEMBER:     (1, '\n.. c:member:: {ttype} {name}\n\n{text}\n'),
    Type.MACRO:      (1, '\n.. c:macro:: {name}\n\n{text}\n'),
    Type.MACRO_FUNC: (1, '\n.. c:function:: {name}({args})\n\n{text}\n'),
    Type.FUNC:       (1, '\n.. c:function:: {ttype} {name}({args})\n\n{text}\n')
}

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

def generate(text, fmt=Type.TEXT, name=None,
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

    if transform:
        text = transform(text)

    if args is not None:
        args = ', '.join(args)

    (text_indent, fmt) = _doc_fmt[fmt]
    text = nest(text, text_indent)
    return fmt.format(text=text, name=name, ttype=ttype, args=args)
