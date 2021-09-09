# Copyright (c) 2021 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

from hawkmoth.util import docstr

class Docstring():
    def __init__(self, text, fmt=docstr.Type.TEXT, name=None, ttype=None, args=None, meta=None, nest=0):
        self._text = text
        self._fmt = fmt
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
