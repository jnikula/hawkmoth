# Copyright (c) 2021 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

from hawkmoth.util import docstr

class Docstring():
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

        rst = docstr.generate(text=self._text, indent=self._indent, fmt=self._fmt, name=self._name, ttype=self._ttype,
                              args=self._args, transform=transform)

        rst = docstr.nest(rst, self._nest)

        return rst

    def get_meta(self):
        return self._meta

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
