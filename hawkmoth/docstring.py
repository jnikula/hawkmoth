# Copyright (c) 2021 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

class Docstring():
    def __init__(self, doc, meta):
        self._doc = doc
        self._meta = meta

    def get_docstring(self):
        return self._doc

    def get_meta(self):
        return self._meta

    def get_line(self):
        return self._meta['line']
