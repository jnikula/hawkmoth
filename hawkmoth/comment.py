# Copyright (c) 2021 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

from hawkmoth.util import docstr

class Comment():
    def __init__(self, text, name=None, ttype=None, args=None, meta=None, nest=0):
        self.text = text
        self.name = name
        self.ttype = ttype
        self.args = args
        self.meta = meta
        self.nest = nest

    def get_rst(self, transform=None):
        # FIXME: docstr.generate changes the number of lines in output. This
        # impacts the error reporting via meta['line']. Adjust meta to take this
        # into account.

        rst = docstr.generate(text=self.text, indent=self.indent, fmt=self.fmt, name=self.name, ttype=self.ttype,
                              args=self.args, transform=transform)

        rst = docstr.nest(rst, self.nest)

        return rst

    def get_meta(self):
        return self.meta

    def get_line(self):
        return self.meta['line']

class TextComment(Comment):
    indent = 0
    fmt = '\n{text}\n'

class VarComment(Comment):
    indent = 1
    fmt = '\n.. c:var:: {ttype} {name}\n\n{text}\n'

class TypeComment(Comment):
    indent = 1
    fmt = '\n.. c:type:: {name}\n\n{text}\n'

class StructComment(Comment):
    indent = 1
    fmt = '\n.. c:struct:: {name}\n\n{text}\n'

class UnionComment(Comment):
    indent = 1
    fmt = '\n.. c:union:: {name}\n\n{text}\n'

class EnumComment(Comment):
    indent = 1
    fmt = '\n.. c:enum:: {name}\n\n{text}\n'

class EnumValComment(Comment):
    indent = 1
    fmt = '\n.. c:enumerator:: {name}\n\n{text}\n'

class MemberComment(Comment):
    indent = 1
    fmt = '\n.. c:member:: {ttype} {name}\n\n{text}\n'

class MacroComment(Comment):
    indent = 1
    fmt = '\n.. c:macro:: {name}\n\n{text}\n'

class MacroFuncComment(Comment):
    indent = 1
    fmt = '\n.. c:macro:: {name}({args})\n\n{text}\n'

class FuncComment(Comment):
    indent = 1
    fmt = '\n.. c:function:: {ttype} {name}({args})\n\n{text}\n'
