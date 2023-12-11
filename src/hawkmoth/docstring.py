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

    def __init__(self, cursor=None, text=None, meta=None, nest=0):
        if cursor:
            self._args = cursor.args
            self._decl_name = cursor.decl_name
            self._domain = cursor.domain
            self._meta = cursor.meta
            self._name = cursor.name
            self._quals = cursor.quals
            self._text = cursor.comment
            self._ttype = cursor.type
        else:
            self._args = None
            self._decl_name = None
            self._domain = None
            self._meta = meta
            self._name = None
            self._quals = None
            self._text = text
            self._ttype = None

        self._nest = nest
        self._children = []

    def _match(self, filter_types=None, filter_names=None):
        if filter_types is not None and type(self) not in filter_types:
            return False

        if filter_names is not None and self.get_name() not in filter_names:
            return False

        return True

    def walk(self, recurse=True, filter_types=None, filter_names=None):
        if self._text:
            yield self

    @staticmethod
    def is_doc(comment):
        """Test if comment is a C documentation comment."""
        return comment.startswith('/**') and comment != '/**/'

    def _get_header_lines(self):
        name = self._get_decl_name()
        domain = self._domain

        header = self._fmt.format(domain=domain, name=name)

        return header.splitlines()

    def _get_comment_lines(self):
        return statemachine.string2lines(self._text, 8, convert_whitespace=True)

    @staticmethod
    def _remove_comment_markers(lines):
        """Remove comment markers and line prefixes from comment lines.

        Return the number of lines removed from the beginning.
        """
        line_offset = 0

        lines[0] = re.sub(r'^/\*\*[ \t]*', '', lines[0])
        lines[-1] = re.sub(r'[ \t]*\*/$', '', lines[-1])

        prefix_len = _get_prefix_len(lines[1:-1])
        lines[1:-1] = [line[prefix_len:] for line in lines[1:-1]]

        while lines and (not lines[0] or lines[0].isspace()):
            line_offset += 1
            del lines[0]

        while lines and (not lines[-1] or lines[-1].isspace()):
            del lines[-1]

        return line_offset

    @staticmethod
    def _nest_lines(lines, nest):
        """
        Indent documentation block for nesting.

        Args:
            lines (List[str]): Documentation body as list of strings,
                modified in-place.
            nest (int): Nesting level. For each level, the final block is indented
                one level. Useful for (e.g.) declaring structure members.
        """
        lines[:] = ['   ' * nest + line if line else '' for line in lines]

    def get_docstring(self, process_docstring=None):
        header_lines = self._get_header_lines()
        comment_lines = self._get_comment_lines()

        line_offset = Docstring._remove_comment_markers(comment_lines)

        if process_docstring is not None:
            process_docstring(comment_lines)

        Docstring._nest_lines(comment_lines, self._indent)

        # ensure we have cushion blank line before the docstring
        if len(header_lines) == 0 or header_lines[0] != '':
            header_lines.insert(0, '')

        # ensure we have cushion blank line between header and comment
        if header_lines[-1] != '':
            header_lines.append('')

        line_offset -= len(header_lines)

        lines = header_lines + comment_lines

        Docstring._nest_lines(lines, self._nest)

        # ensure we have cushion blank line after the docstring
        if lines[-1] != '':
            lines.append('')

        return lines, self.get_line() + line_offset

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
    _fmt = ''

    def get_name(self):
        """Figure out a name for the text comment based on the comment contents.

        The name is the sub-string starting from the first alphanumeric
        character in the comment to the next :, ., or newline.

        This sensibly covers cases like reStructuredText hyperlink targets::

            .. _Foo Bar:

        and section titles::

            Foo Bar
            =======

        and just first sentences::

            Foo Bar. Blah.

        Not perfect, but good enough.
        """
        # If the parser passed in a name, use it (unlikely)
        if self._name:
            return self._name

        mo = re.search(r'[\W_]*(?P<name>\w[^:.\n\r]*)', self._text)

        return mo.group('name') if mo else None

class VarDocstring(Docstring):
    _indent = 1
    _fmt = '.. {domain}:var:: {ttype}{type_spacer}{name}'

    def _get_header_lines(self):
        name = self._get_decl_name()
        domain = self._domain
        ttype = self._ttype

        type_spacer = ''
        if ttype and not (len(ttype) == 0 or ttype.endswith('*')):
            type_spacer = ' '

        header = self._fmt.format(domain=domain, name=name, ttype=ttype,
                                  type_spacer=type_spacer)

        return header.splitlines()

class TypedefDocstring(Docstring):
    _indent = 1
    _fmt = '.. {domain}:type:: {name}'

class TypeAliasDocstring(Docstring):
    _indent = 1
    _fmt = '.. cpp:type:: {name} = {underlying_type}'

    def __init__(self, cursor, nest):
        self._underlying_type = cursor.value
        super().__init__(cursor=cursor, nest=nest)

    def _get_header_lines(self):
        name = self._get_decl_name()
        underlying_type = self._underlying_type.spelling

        header = self._fmt.format(name=name, underlying_type=underlying_type)

        return header.splitlines()

class _CompoundDocstring(Docstring):
    def _get_decl_name(self):
        # If decl_name is empty, it means this is an anonymous declaration.
        if self._decl_name is None:
            # Sphinx expects @name for anonymous entities. The name must be both
            # stable and unique. Create one.
            decl_name = hashlib.md5(f'{self._text}{self.get_line()}'.encode()).hexdigest()

            return f'@anonymous_{decl_name}'

        return self._decl_name

    def add_child(self, comment):
        self._children.append(comment)

    def add_children(self, comments):
        self._children.extend(comments)

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

class RootDocstring(_CompoundDocstring):
    def __init__(self, filename=None, domain='c', clang_args=None):
        super().__init__()
        self._filename = filename
        self._domain = domain
        self._clang_args = clang_args

    def get_filename(self):
        return self._filename

    def get_clang_args(self):
        return self._clang_args

    def get_domain(self):
        return self._domain

class StructDocstring(_CompoundDocstring):
    _indent = 1
    _fmt = '.. {domain}:struct:: {name}'

class UnionDocstring(_CompoundDocstring):
    _indent = 1
    _fmt = '.. {domain}:union:: {name}'

class EnumDocstring(_CompoundDocstring):
    _indent = 1
    _fmt = '.. {domain}:enum:: {name}'

class EnumeratorDocstring(Docstring):
    _indent = 1
    _fmt = '.. {domain}:enumerator:: {name}{value}'

    def __init__(self, cursor, nest=0):
        self._value = cursor.value
        super().__init__(cursor=cursor, nest=nest)

    def _get_header_lines(self):
        value = f' = {self._value}' if self._value is not None else ''
        header = self._fmt.format(domain=self._domain, name=self._get_decl_name(),
                                  value=value)

        return header.splitlines()

class MemberDocstring(Docstring):
    _indent = 1
    _fmt = '.. {domain}:member:: {ttype}{type_spacer}{name}'

    def _get_header_lines(self):
        name = self._get_decl_name()
        domain = self._domain
        ttype = self._ttype

        type_spacer = ''
        if ttype and not (len(ttype) == 0 or ttype.endswith('*')):
            type_spacer = ' '

        header = self._fmt.format(domain=domain, name=name, ttype=ttype,
                                  type_spacer=type_spacer)

        return header.splitlines()

class MacroDocstring(Docstring):
    _indent = 1
    _fmt = '.. c:macro:: {name}'

class MacroFunctionDocstring(Docstring):
    _indent = 1
    _fmt = '.. c:macro:: {name}({args})'

    def _get_header_lines(self):
        name = self._get_decl_name()
        args = ', '.join([n for _, n in self._args])

        header = self._fmt.format(name=name, args=args)

        return header.splitlines()

class FunctionDocstring(Docstring):
    _indent = 1
    _fmt = '.. {domain}:function:: {ttype}{type_spacer}{name}({args}){quals_spacer}{quals}'

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
            def pad_type(t): return '' if len(t) == 0 or t.endswith('*') or t.endswith('&') else ' '
            def arg_fmt(t, n): return f'{t}{pad_type(t)}{n}'
            args = ', '.join([arg_fmt(t, n) for t, n in self._args])

        header = self._fmt.format(domain=domain, name=name, ttype=ttype,
                                  type_spacer=type_spacer, args=args,
                                  quals=quals, quals_spacer=quals_spacer)

        return header.splitlines()

class ClassDocstring(_CompoundDocstring):
    _indent = 1
    _fmt = '.. cpp:class:: {name}'

class EnumClassDocstring(_CompoundDocstring):
    _indent = 1
    _fmt = '.. cpp:enum-class:: {name}'
