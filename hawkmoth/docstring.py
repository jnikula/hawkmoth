# Copyright (c) 2016-2021 Jani Nikula <jani@nikula.org>
# Copyright (c) 2018-2020 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Documentation comment storage and converter
===========================================

Class hierarchy for storing a tree of different types of documentation
comments.

The documentation comments from C source are stored verbatim. There are methods
for walking the documentation comment tree and returning the documentation with
conversions:

* Stripping the comment delimiters (``/**`` and ``*/``) and continuation
  line prefixes (e.g. ``␣*␣``).

* Optional transformation of the documentation comments to support different
  syntaxes. These filters are expected to translate the comment into
  reStructuredText.

* Generation of Sphinx C Domain directives with appropriate indentation.
"""

import re

class Docstring():
    _indent = 0
    _fmt = ''

    def __init__(self, text=None, name=None, decl_name=None, ttype=None, args=None, meta=None, nest=0):
        self._text = text
        self._name = name
        self._decl_name = decl_name if decl_name else name
        self._ttype = ttype
        self._args = args
        self._meta = meta
        self._nest = nest
        self._children = []

    def add_child(self, comment):
        self._children.append(comment)

    def add_children(self, comments):
        self._children.extend(comments)

    def walk(self, recurse=True):
        # The contents of the parent will always be before children.
        if self._text:
            yield self

        # Sort the children by order of appearance. We may add other sort
        # options later.
        for comment in sorted(self._children, key=lambda c: c.get_line()):
            if recurse:
                yield from comment.walk()
            else:
                yield comment

    @staticmethod
    def is_doc(comment):
        """Test if comment is a C documentation comment."""
        return comment.startswith('/**') and comment != '/**/'

    @staticmethod
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

    @staticmethod
    def _nest(text, nest):
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

    def get_docstring(self, transform=None):
        # FIXME: This changes the number of lines in output. This impacts the
        # error reporting via meta['line']. Adjust meta to take this into
        # account.

        text = Docstring._strip(self._text)

        if transform is not None:
            text = transform(text)

        text = Docstring._nest(text, self._indent)

        args = ', '.join(self._args) if self._args is not None else None

        rst = self._fmt.format(text=text, name=self._decl_name, ttype=self._ttype, args=args)

        rst = Docstring._nest(rst, self._nest)

        return rst

    def get_meta(self):
        return self._meta

    def get_name(self):
        return self._name

    def get_line(self):
        return self._meta['line']

class TextDocstring(Docstring):
    _indent = 0
    _fmt = '\n{text}\n'

class VarDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:var:: {ttype} {name}\n\n{text}\n'

class TypeDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:type:: {name}\n\n{text}\n'

class StructDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:struct:: {name}\n\n{text}\n'

class UnionDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:union:: {name}\n\n{text}\n'

class EnumDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:enum:: {name}\n\n{text}\n'

class EnumeratorDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:enumerator:: {name}\n\n{text}\n'

class MemberDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:member:: {ttype} {name}\n\n{text}\n'

class MacroDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:macro:: {name}\n\n{text}\n'

class MacroFunctionDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:macro:: {name}({args})\n\n{text}\n'

class FunctionDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:function:: {ttype} {name}({args})\n\n{text}\n'
