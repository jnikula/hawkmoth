# Copyright (c) 2021 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

from hawkmoth.util import docstr

class Docstring():
    _fmt = docstr.Type.TEXT

    def __init__(self, text, name=None, ttype=None, args=None, meta=None, nest=0):
        self._text = text
        self._name = name
        self._ttype = ttype
        self._args = args
        self._meta = meta
        self._nest = nest

    def get_docstring(self, transform=None):
        # FIXME: docstr.generate changes the number of lines in output. This
        # impacts the error reporting via meta['line']. Adjust meta to take this
        # into account.

        rst = docstr.generate(text=self._text, fmt=self._fmt, name=self._name, ttype=self._ttype,
                              args=self._args, transform=transform)

        rst = docstr.nest(rst, self._nest)

        return rst

    def get_meta(self):
        return self._meta

    def get_line(self):
        return self._meta['line']

class TextDocstring(Docstring):
    _fmt = docstr.Type.TEXT

class VarDocstring(Docstring):
    _fmt = docstr.Type.VAR

class TypeDocstring(Docstring):
    _fmt = docstr.Type.TYPE

class StructDocstring(Docstring):
    _fmt = docstr.Type.STRUCT

class UnionDocstring(Docstring):
    _fmt = docstr.Type.UNION

class EnumDocstring(Docstring):
    _fmt = docstr.Type.ENUM

class EnumeratorDocstring(Docstring):
    _fmt = docstr.Type.ENUM_VAL

class MemberDocstring(Docstring):
    _fmt = docstr.Type.MEMBER

class MacroDocstring(Docstring):
    _fmt = docstr.Type.MACRO

class MacroFunctionDocstring(Docstring):
    _fmt = docstr.Type.MACRO_FUNC

class FunctionDocstring(Docstring):
    _fmt = docstr.Type.FUNC
