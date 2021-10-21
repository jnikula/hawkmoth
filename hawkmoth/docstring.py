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

import hashlib
import os
import re

def _commonprefix_len(lines):
    # common prefix
    prefix = os.path.commonprefix(lines)

    # common prefix length of limited characters
    return len(prefix) - len(prefix.lstrip(' \t*'))

def _get_prefix_len(lines):
    # ignore lines with just space
    lines = [line for line in lines if line.strip()]
    prefix_len = _commonprefix_len(lines)

    # ignore lines with just the prefix and space
    lines = [line for line in lines if line[prefix_len:].strip()]
    prefix_len = _commonprefix_len(lines)

    return prefix_len

class Docstring():
    _indent = 0
    _fmt = ''

    def __init__(self, text=None, name=None, decl_name=None,
                 ttype=None, args=None, meta=None, nest=0):
        self._text = text
        self._name = name
        self._decl_name = decl_name
        self._ttype = ttype
        self._args = args
        self._meta = meta
        self._nest = nest
        self._children = []

    def add_child(self, comment):
        self._children.append(comment)

    def add_children(self, comments):
        self._children.extend(comments)

    def _match(self, filter_types=None, filter_names=None):
        if filter_types is not None and type(self) not in filter_types:
            return False

        if filter_names is not None and self.get_name() not in filter_names:
            return False

        return True

    def walk(self, recurse=True, filter_types=None, filter_names=None):
        # Note: The filtering is pretty specialized for our use case here. It
        # only filters the immediate children, not this comment, nor
        # grandchildren.

        # The contents of the parent will always be before children.
        if self._text:
            yield self

        # Sort the children by order of appearance. We may add other sort
        # options later.
        for comment in sorted(self._children, key=lambda c: c.get_line()):
            if comment._match(filter_types=filter_types, filter_names=filter_names):
                if recurse:
                    yield from comment.walk()
                else:
                    yield comment

    @staticmethod
    def is_doc(comment):
        """Test if comment is a C documentation comment."""
        return comment.startswith('/**') and comment != '/**/'

    def _get_plain_comment(self):
        """Return plain comment with comment markers and line prefixes removed."""
        lines = self._text.splitlines()

        lines[0] = re.sub(r'^/\*\*[ \t]*', '', lines[0])
        lines[-1] = re.sub(r'[ \t]*\*/$', '', lines[-1])

        prefix_len = _get_prefix_len(lines[1:-1])
        lines[1:-1] = [line[prefix_len:] for line in lines[1:-1]]

        while not lines[0] or lines[0].isspace():
            del lines[0]

        while not lines[-1] or lines[-1].isspace():
            del lines[-1]

        return '\n'.join(lines)

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

        text = self._get_plain_comment()

        if transform is not None:
            text = transform(text)

        text = Docstring._nest(text, self._indent)

        args = ', '.join(self._args) if self._args is not None else None

        rst = self._fmt.format(text=text, name=self._get_decl_name(), ttype=self._ttype, args=args)

        rst = Docstring._nest(rst, self._nest)

        return rst

    def get_meta(self):
        return self._meta

    def _get_decl_name(self):
        return self._decl_name if self._decl_name else self._name

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

class _CompoundDocstring(Docstring):
    def _get_decl_name(self):
        # The empty string for decl_name means anonymous.
        if self._decl_name == '':
            # Sphinx expects @name for anonymous entities. The name must be both
            # stable and unique. Create one.
            decl_name = hashlib.md5(f'{self._text}{self.get_line()}'.encode()).hexdigest()

            return f'@anonymous_{decl_name}'

        return super()._get_decl_name()

class StructDocstring(_CompoundDocstring):
    _indent = 1
    _fmt = '\n.. c:struct:: {name}\n\n{text}\n'

class UnionDocstring(_CompoundDocstring):
    _indent = 1
    _fmt = '\n.. c:union:: {name}\n\n{text}\n'

class EnumDocstring(_CompoundDocstring):
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
