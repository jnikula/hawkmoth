# coding=utf-8
"""Hawkmoth - Sphinx C Domain autodoc directive extension"""

__author__ = "Jani Nikula <jani@nikula.org>"
__copyright__ = "Copyright (c) 2016-2017, Jani Nikula <jani@nikula.org>"
__version__  = '0.1'
__license__ = "BSD 2-Clause, see LICENSE for details"

import glob
import os
import re
import stat
import subprocess
import sys

from docutils import nodes, statemachine
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from sphinx.ext.autodoc import AutodocReporter
from sphinx.util.compat import Directive

# The parser bits
from hawkmoth import parse

# This is the part that interfaces with Sphinx. Do not depend on Clang here.

class CAutoDocDirective(Directive):
    """Extract documentation comments from the specified file"""
    required_argument = 1
    optional_arguments = 1

    # Allow passing a variable number of file patterns as arguments
    final_argument_whitespace = True

    option_spec = {
        'compat': directives.unchanged_required,
        'clang': directives.unchanged_required,
    }
    has_content = False

    def parse(self, viewlist, filename, compat, clang):
        comments = parse(filename, compat=compat, clang=clang)

        for (comment, meta) in comments:
            lineoffset = meta['line']
            lines = statemachine.string2lines(comment, 8, convert_whitespace=True)
            for line in lines:
                viewlist.append(line, filename, lineoffset)
                lineoffset += 1

    def run(self):
        env = self.state.document.settings.env

        compat = self.options.get('compat', env.config.cautodoc_compat)
        clang = self.options.get('clang', env.config.cautodoc_clang)

        result = ViewList()

        for pattern in self.arguments[0].split():
            filenames = glob.glob(env.config.cautodoc_root + '/' + pattern)
            if len(filenames) == 0:
                env.app.warn('Pattern "%s" does not match any files.' %
                             (pattern), location=(env.docname, self.lineno))
                continue

            for filename in filenames:
                mode = os.stat(filename).st_mode
                if stat.S_ISDIR(mode):
                    env.app.warn('Path "%s" matching pattern "%s" is a directory.' %
                                 (filename, pattern),
                                 location=(env.docname, self.lineno))
                    continue

                # Tell Sphinx about the dependency
                env.note_dependency(os.path.abspath(filename))
                self.parse(result, filename, compat, clang)

        node = nodes.section()
        node.document = self.state.document
        self.state.nested_parse(result, self.content_offset, node)

        return node.children

def setup(app):
    app.require_sphinx('1.3')
    app.add_config_value('cautodoc_root', app.confdir, 'env')
    app.add_config_value('cautodoc_compat', None, 'env')
    app.add_config_value('cautodoc_clang', None, 'env')
    app.add_directive_to_domain('c', 'autodoc', CAutoDocDirective)

    return dict(version = __version__,
                parallel_read_safe = True, parallel_write_safe = True)
