# Copyright (c) 2016-2021 Jani Nikula <jani@nikula.org>
# Copyright (c) 2018-2023 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
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

from docutils import statemachine

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

    def __init__(self, domain='c', text=None, name=None,
                 decl_name=None, ttype=None, args=None,
                 quals=None, meta=None, nest=0):
        self._text = text
        self._name = name
        self._decl_name = decl_name
        self._ttype = ttype
        self._args = args
        self._quals = quals
        self._meta = meta
        self._nest = nest
        self._domain = domain
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

    def _get_header_lines(self):
        name = self._get_decl_name()
        domain = self._domain
        ttype = self._ttype
        quals = self._quals

        type_spacer = ''
        if ttype and not (len(ttype) == 0 or ttype.endswith('*')):
            type_spacer = ' '

        quals_spacer = ''
        if quals and len(quals) > 0:
            quals_spacer = ' '

        args = ''
        if self._args and len(self._args) > 0:
            pad_type = lambda t: '' if len(t) == 0 or t.endswith('*') or t.endswith('&') else ' '
            arg_fmt = lambda t, n: f"{t}{pad_type(t)}{n}"
            args = ', '.join([arg_fmt(t, n) for t, n in self._args])

        header = self._fmt.format(domain=domain, name=name, ttype=ttype,
                                  type_spacer=type_spacer, args=args,
                                  quals=quals, quals_spacer=quals_spacer)

        return header.splitlines()

    def _get_comment_lines(self):
        return statemachine.string2lines(self._text, 8, convert_whitespace=True)

    @staticmethod
    def _remove_comment_markers(lines):
        """Remove comment markers and line prefixes from comment lines."""
        lines[0] = re.sub(r'^/\*\*[ \t]*', '', lines[0])
        lines[-1] = re.sub(r'[ \t]*\*/$', '', lines[-1])

        prefix_len = _get_prefix_len(lines[1:-1])
        lines[1:-1] = [line[prefix_len:] for line in lines[1:-1]]

        while not lines[0] or lines[0].isspace():
            del lines[0]

        while not lines[-1] or lines[-1].isspace():
            del lines[-1]

    @staticmethod
    def _nest(lines, nest):
        """
        Indent documentation block for nesting.

        Args:
            lines (List[str]): Documentation body as list of strings,
                modified in-place.
            nest (int): Nesting level. For each level, the final block is indented
                one level. Useful for (e.g.) declaring structure members.
        """
        lines[:] = ['   ' * nest + line if line else '' for line in lines]

    def get_docstring(self, transform=None):
        header_lines = self._get_header_lines()
        comment_lines = self._get_comment_lines()

        # FIXME: This changes the number of lines in output. This impacts the
        # error reporting via meta['line']. Adjust meta to take this into
        # account.
        Docstring._remove_comment_markers(comment_lines)

        if transform is not None:
            transform(comment_lines)

        Docstring._nest(comment_lines, self._indent)

        lines = header_lines + comment_lines

        Docstring._nest(lines, self._nest)

        if lines[-1] != '':
            lines.append('')

        return lines

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
    _fmt = '\n'

class VarDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. {domain}:var:: {ttype}{type_spacer}{name}\n\n'

class TypeDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. {domain}:type:: {name}\n\n'

class _CompoundDocstring(Docstring):
    def _get_decl_name(self):
        # If decl_name is empty, it means this is an anonymous declaration.
        if self._decl_name is None:
            # Sphinx expects @name for anonymous entities. The name must be both
            # stable and unique. Create one.
            decl_name = hashlib.md5(f'{self._text}{self.get_line()}'.encode()).hexdigest()

            return f'@anonymous_{decl_name}'

        return self._decl_name

class StructDocstring(_CompoundDocstring):
    _indent = 1
    _fmt = '\n.. {domain}:struct:: {name}\n\n'

class UnionDocstring(_CompoundDocstring):
    _indent = 1
    _fmt = '\n.. {domain}:union:: {name}\n\n'

class EnumDocstring(_CompoundDocstring):
    _indent = 1
    _fmt = '\n.. {domain}:enum:: {name}\n\n'

class EnumeratorDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. {domain}:enumerator:: {name}\n\n'

class MemberDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. {domain}:member:: {ttype}{type_spacer}{name}\n\n'

class MacroDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:macro:: {name}\n\n'

class MacroFunctionDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. c:macro:: {name}({args})\n\n'

class FunctionDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. {domain}:function:: {ttype}{type_spacer}{name}({args}){quals_spacer}{quals}\n\n'

class ClassDocstring(_CompoundDocstring):
    _indent = 1
    _fmt = '\n.. cpp:class:: {name}\n\n'

class EnumClassDocstring(Docstring):
    _indent = 1
    _fmt = '\n.. cpp:enum-class:: {name}\n\n'
