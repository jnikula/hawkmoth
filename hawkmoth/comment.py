# Copyright (c) 2021 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

from hawkmoth.util import docstr

class Comment():
    def __init__(self, text, fmt=docstr.Type.TEXT, name=None, ttype=None, args=None, meta=None, nest=0):
        self.text = text
        self.fmt = fmt
        self.name = name
        self.ttype = ttype
        self.args = args
        self.meta = meta
        self.nest = nest

    def get_rst(self, transform=None):
        # FIXME: docstr.generate changes the number of lines in output. This
        # impacts the error reporting via meta['line']. Adjust meta to take this
        # into account.

        rst = docstr.generate(text=self.text, fmt=self.fmt, name=self.name, ttype=self.ttype,
                              args=self.args, transform=transform)

        rst = docstr.nest(rst, self.nest)

        return rst

    def get_meta(self):
        return self.meta

    def get_line(self):
        return self.meta['line']
