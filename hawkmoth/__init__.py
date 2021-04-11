# Copyright (c) 2016-2017, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Hawkmoth
========

Sphinx C Domain autodoc directive extension.
"""

import glob
import os
import re
import stat
import subprocess
import sys

from docutils import nodes, statemachine
from docutils.parsers.rst import directives, Directive
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util.docutils import switch_source_input
from sphinx.util import logging

from hawkmoth.parser import parse, ErrorLevel
from hawkmoth.util import doccompat, strutil

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'VERSION')) as version_file:
    __version__ = version_file.read().strip()

class CAutoDocDirective(Directive):
    """Extract all documentation comments from the specified file"""
    required_argument = 1
    optional_arguments = 1
    logger = logging.getLogger(__name__)

    # Allow passing a variable number of file patterns as arguments
    final_argument_whitespace = True

    option_spec = {
        'transform': directives.unchanged_required,
        'compat': directives.unchanged_required,
        'clang': directives.unchanged_required,
    }
    has_content = False

    # Map verbosity levels to logger levels.
    _log_lvl = {ErrorLevel.ERROR: logging.LEVEL_NAMES['ERROR'],
                ErrorLevel.WARNING: logging.LEVEL_NAMES['WARNING'],
                ErrorLevel.INFO: logging.LEVEL_NAMES['INFO'],
                ErrorLevel.DEBUG: logging.LEVEL_NAMES['DEBUG']}

    def __display_parser_diagnostics(self, errors):
        env = self.state.document.settings.env

        for (severity, filename, lineno, msg) in errors:
            if filename:
                toprint = f'{filename}:{lineno}: {msg}'
            else:
                toprint = f'{msg}'

            if severity.value <= env.app.verbosity:
                self.logger.log(self._log_lvl[severity], toprint,
                                location=(env.docname, self.lineno))

    def __get_clang_args(self):
        env = self.state.document.settings.env

        clang_args = env.config.cautodoc_clang.copy()

        clang_args.extend(strutil.args_as_list(self.options.get('clang')))

        return clang_args

    def __get_compat_transform(self):
        env = self.state.document.settings.env

        compat = self.options.get('compat', env.config.cautodoc_compat)
        if compat is None:
            return None

        fmt = 'cautodoc_compat and compat options are deprecated, please use cautodoc_transformations and transform options instead.'
        self.logger.warning(fmt, location=(env.docname, self.lineno))

        return lambda comment: doccompat.convert(comment, transform=compat)

    def __get_transform(self):
        env = self.state.document.settings.env

        # Handle deprecated compat. To be removed.
        transform = self.__get_compat_transform()
        if transform is not None:
            return transform

        transformations = env.config.cautodoc_transformations
        tropt = self.options.get('transform')

        if transformations is None:
            if tropt is not None:
                self.logger.warning('transform specified without cautodoc_transformations config.',
                                    location=(env.docname, self.lineno))

            return None

        # Note: None is a valid key for default.
        if tropt not in transformations:
            if tropt is not None:
                self.logger.warning(f'unknown transformation "{tropt}".',
                                    location=(env.docname, self.lineno))
            return None

        # Note: None is a valid value for no transformation.
        return transformations.get(tropt)

    def __parse(self, viewlist, filename):
        env = self.state.document.settings.env

        clang_args = self.__get_clang_args()
        transform = self.__get_transform()

        comments, errors = parse(filename, transform=transform, clang=clang_args)

        self.__display_parser_diagnostics(errors)

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
                self.logger.warning(f'Pattern "{pattern}" does not match any files.',
                                    location=(env.docname, self.lineno))
                continue

            for filename in filenames:
                mode = os.stat(filename).st_mode
                if stat.S_ISDIR(mode):
                    self.logger.warning(f'Path "{filename}" matching pattern "{pattern}" is a directory.',
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
    app.require_sphinx('3.0')
    app.add_config_value('cautodoc_root', app.confdir, 'env', [str])
    app.add_config_value('cautodoc_compat', None, 'env', [str])
    app.add_config_value('cautodoc_transformations', None, 'env', [dict])
    app.add_config_value('cautodoc_clang', [], 'env', [list])
    app.add_directive_to_domain('c', 'autodoc', CAutoDocDirective)

    return dict(version = __version__,
                parallel_read_safe = True, parallel_write_safe = True)
