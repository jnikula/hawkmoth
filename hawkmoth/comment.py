# Copyright (c) 2021 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

class Comment():
    def __init__(self, doc, meta):
        self.doc = doc
        self.meta = meta

    def get_rst(self):
        return self.doc

    def get_meta(self):
        return self.meta

    def get_line(self):
        return self.meta['line']
