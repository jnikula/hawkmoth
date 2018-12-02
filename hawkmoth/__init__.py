# Copyright (c) 2016-2017, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Hawkmoth
========

Sphinx C Domain autodoc directive extension.
"""

__version__  = '0.1'

import glob
import os
import re
import stat
import subprocess
import sys

from docutils import nodes, statemachine
from docutils.parsers.rst import directives, Directive
from docutils.statemachine import ViewList
from sphinx.ext.autodoc import AutodocReporter
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util.docutils import switch_source_input

# The parser bits
from . import hawkmoth

class CAutoDocDirective(Directive):
    """Extract all documentation comments from the specified file"""
    required_argument = 1
    optional_arguments = 1

    # Allow passing a variable number of file patterns as arguments
    final_argument_whitespace = True

    option_spec = {
        'compat': directives.unchanged_required,
        'clang': directives.unchanged_required,
    }
    has_content = False

    def __parse(self, viewlist, filename):
        env = self.state.document.settings.env

        compat = self.options.get('compat', env.config.cautodoc_compat)
        clang = self.options.get('clang', env.config.cautodoc_clang)

        comments = hawkmoth.parse(filename, compat=compat, clang=clang)

        for (comment, meta) in comments:
            lineoffset = meta['line'] - 1
            lines = statemachine.string2lines(comment, 8,
                                              convert_whitespace=True)
            for line in lines:
                viewlist.append(line, filename, lineoffset)
                lineoffset += 1

    def run(self):
        env = self.state.document.settings.env

        result = ViewList()

        for pattern in self.arguments[0].split():
            filenames = glob.glob(env.config.cautodoc_root + '/' + pattern)
            if len(filenames) == 0:
                fmt = 'Pattern "{pat}" does not match any files.'
                env.app.warn(fmt.format(pattern),
                             location=(env.docname, self.lineno))
                continue

            for filename in filenames:
                mode = os.stat(filename).st_mode
                if stat.S_ISDIR(mode):
                    fmt = 'Path "{name}" matching pattern "{pat}" is a directory.'
                    env.app.warn(fmt.format(name=filename, pat=pattern),
                                 location=(env.docname, self.lineno))
                    continue

                # Tell Sphinx about the dependency and parse the file
                env.note_dependency(os.path.abspath(filename))
                self.__parse(result, filename)

        # Parse the extracted reST
        with switch_source_input(self.state, result):
            node = nodes.section()
            nested_parse_with_titles(self.state, result, node)

        return node.children

def setup(app):
    app.require_sphinx('1.8')
    app.add_config_value('cautodoc_root', app.confdir, 'env')
    app.add_config_value('cautodoc_compat', None, 'env')
    app.add_config_value('cautodoc_clang', None, 'env')
    app.add_directive_to_domain('c', 'autodoc', CAutoDocDirective)

    return dict(version = __version__,
                parallel_read_safe = True, parallel_write_safe = True)
