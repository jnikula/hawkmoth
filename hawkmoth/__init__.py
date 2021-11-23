# Copyright (c) 2016-2017, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Hawkmoth
========

Sphinx C Domain autodoc directive extension.
"""

import glob
import os

from docutils import nodes, statemachine
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util.docutils import switch_source_input, SphinxDirective
from sphinx.util import logging

from hawkmoth.parser import parse, ErrorLevel
from hawkmoth.util import doccompat, strutil
from hawkmoth import docstring

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'VERSION')) as version_file:
    __version__ = version_file.read().strip()

class CAutoBaseDirective(SphinxDirective):
    logger = logging.getLogger(__name__)

    option_spec = {
        'transform': directives.unchanged_required,
        'compat': directives.unchanged_required,
        'clang': strutil.string_list,
    }
    has_content = False

    _docstring_types = None

    # Map verbosity levels to logger levels.
    _log_lvl = {ErrorLevel.ERROR: logging.LEVEL_NAMES['ERROR'],
                ErrorLevel.WARNING: logging.LEVEL_NAMES['WARNING'],
                ErrorLevel.INFO: logging.LEVEL_NAMES['INFO'],
                ErrorLevel.DEBUG: logging.LEVEL_NAMES['DEBUG']}

    def __display_parser_diagnostics(self, errors):
        for (severity, filename, lineno, msg) in errors:
            if filename:
                toprint = f'{filename}:{lineno}: {msg}'
            else:
                toprint = f'{msg}'

            if severity.value <= self.env.app.verbosity:
                self.logger.log(self._log_lvl[severity], toprint,
                                location=(self.env.docname, self.lineno))

    def __get_clang_args(self):
        clang_args = self.env.config.cautodoc_clang.copy()

        clang_args.extend(self.options.get('clang', []))

        return clang_args

    def __get_compat_transform(self):
        compat = self.options.get('compat', self.env.config.cautodoc_compat)
        if compat is None:
            return None

        fmt = 'cautodoc_compat and compat options are deprecated, please use cautodoc_transformations and transform options instead.'  # noqa: E501
        self.logger.warning(fmt, location=(self.env.docname, self.lineno))

        return lambda comment: doccompat.convert(comment, transform=compat)

    def __get_transform(self):
        # Handle deprecated compat. To be removed.
        transform = self.__get_compat_transform()
        if transform is not None:
            return transform

        transformations = self.env.config.cautodoc_transformations
        tropt = self.options.get('transform')

        if transformations is None:
            if tropt is not None:
                self.logger.warning('transform specified without cautodoc_transformations config.',
                                    location=(self.env.docname, self.lineno))

            return None

        # Note: None is a valid key for default.
        if tropt not in transformations:
            if tropt is not None:
                self.logger.warning(f'unknown transformation "{tropt}".',
                                    location=(self.env.docname, self.lineno))
            return None

        # Note: None is a valid value for no transformation.
        return transformations.get(tropt)

    def __get_docstrings(self, cache, clang_args, viewlist, filename):
        transform = self.__get_transform()
        matched = False

        key = (filename, tuple(clang_args))
        root = cache.get(key, None)

        for docstrings in root.walk(recurse=False, filter_types=self._docstring_types,
                                    filter_names=self._get_names()):
            for docstr in docstrings.walk(filter_names=self._get_members()):
                lineoffset = docstr.get_line() - 1
                lines = statemachine.string2lines(docstr.get_docstring(transform=transform), 8,
                                                  convert_whitespace=True)
                for line in lines:
                    viewlist.append(line, filename, lineoffset)
                    lineoffset += 1

                matched = True

        return matched

    def _get_names(self):
        return None

    def _get_members(self):
        return None

    def _get_filenames(self):
        """
        Return a tuple (auto lookup, list of filenames to use as a search path).

        If the automatic lookup flag is set the list shall be ignored and all
        files within the search path used instead. The flag is important to
        distinguish between `(True, [])` and `(False, [])`  when the filenames
        are a required argument instead of an option and yet there is no match.
        """
        raise NotImplementedError(self.__class__.__name__ + '._get_filenames')

    def __get_all_filenames(self):
        nfiles = 0

        filenames = glob.glob(os.path.join(self.env.config.cautodoc_root, '*.[ch]'))
        filenames += glob.glob(os.path.join(self.env.config.cautodoc_root, '**/*.[ch]'))

        for filename in filenames:
            if os.path.isfile(filename):
                nfiles += 1
                yield os.path.abspath(filename)
        else:
            if nfiles == 0:
                self.logger.warning(f'No source files in {self.env.config.cautodoc_root}.',
                                    location=(self.env.docname, self.lineno))

    def __build_cache(self, cache, clang_args, filename):
        # The output depends on clang args
        key = (filename, tuple(clang_args))

        if key not in cache:
            self.env.note_dependency(filename)

            docstrings, errors = parse(filename, clang_args=clang_args)

            self.__display_parser_diagnostics(errors)
            cache[key] = docstrings

    def run(self):
        clang_args = self.__get_clang_args()
        cache = self.env.temp_data.setdefault('cautodoc_cache', {})
        result = ViewList()
        matches = []

        # If the automatic file name resolution flag is set, use all files in
        # the search path instead for both the cache building and for the member
        # search space.
        auto, filenames = self._get_filenames()
        if auto:
            filenames = self.__get_all_filenames()

        for filename in filenames:
            self.__build_cache(cache, clang_args, filename)
            if self.__get_docstrings(cache, clang_args, result, filename):
                matches.append(filename)

        nmatches = len(matches)
        if nmatches == 0:
            self.logger.warning('No matching docstring.',
                                location=(self.env.docname, self.lineno))
        elif auto and nmatches > 1:
            self.logger.warning(f'Multiple docstring matches in files {matches}.',
                                location=(self.env.docname, self.lineno))

        # Parse the extracted reST
        with switch_source_input(self.state, result):
            node = nodes.section()
            nested_parse_with_titles(self.state, result, node)

        return node.children

class CAutoDocDirective(CAutoBaseDirective):
    """Extract all documentation comments from the specified files"""

    # Allow passing a variable number of file patterns as arguments
    required_arguments = 1
    optional_arguments = 100   # arbitrary limit

    def _get_filenames(self):
        filenames = []

        for pattern in self.arguments:
            candidates = glob.glob(os.path.join(self.env.config.cautodoc_root, pattern))
            if len(candidates) == 0:
                self.logger.warning(f'Pattern "{pattern}" does not match any files.',
                                    location=(self.env.docname, self.lineno))
                continue

            for filename in filenames:
                if os.path.isfile(filename):
                    filenames.append(os.path.abspath(filename))
                else:
                    self.logger.warning(f'Path "{filename}" matching pattern "{pattern}" is not a file.',  # noqa: E501
                                        location=(self.env.docname, self.lineno))

        if len(filenames) == 0:
            self.logger.warning('Directive did not match any source file.',
                                location=(self.env.docname, self.lineno))

        return False, filenames

# Base class for named stuff
class CAutoSymbolDirective(CAutoBaseDirective):
    """Extract specified documentation comments from the specified file"""

    required_arguments = 1
    optional_arguments = 0

    option_spec = CAutoBaseDirective.option_spec.copy()
    option_spec.update({
        'file': directives.unchanged_required,
    })

    def _get_filenames(self):
        filename = self.options.get('file')

        if filename:
            return False, [os.path.abspath(os.path.join(self.env.config.cautodoc_root, filename))]
        else:
            return True, []

    def _get_names(self):
        return [self.arguments[0]]

class CAutoVarDirective(CAutoSymbolDirective):
    _docstring_types = [docstring.VarDocstring]

class CAutoTypeDirective(CAutoSymbolDirective):
    _docstring_types = [docstring.TypeDocstring]

class CAutoMacroDirective(CAutoSymbolDirective):
    _docstring_types = [docstring.MacroDocstring, docstring.MacroFunctionDocstring]

class CAutoFunctionDirective(CAutoSymbolDirective):
    _docstring_types = [docstring.FunctionDocstring]

def members_filter(argument):
    # Use None for members option without an argument to not filter.
    if argument is None:
        return None
    return strutil.string_list(argument)

class CAutoCompoundDirective(CAutoSymbolDirective):
    option_spec = CAutoSymbolDirective.option_spec.copy()
    option_spec.update({
        'members': members_filter,
    })

    def _get_members(self):
        # By default use [] as a filter that does not match any members.
        return self.options.get('members', [])

class CAutoStructDirective(CAutoCompoundDirective):
    _docstring_types = [docstring.StructDocstring]

class CAutoUnionDirective(CAutoCompoundDirective):
    _docstring_types = [docstring.UnionDocstring]

class CAutoEnumDirective(CAutoCompoundDirective):
    _docstring_types = [docstring.EnumDocstring]

def setup(app):
    app.require_sphinx('3.0')
    app.add_config_value('cautodoc_root', app.confdir, 'env', [str])
    app.add_config_value('cautodoc_compat', None, 'env', [str])
    app.add_config_value('cautodoc_transformations', None, 'env', [dict])
    app.add_config_value('cautodoc_clang', [], 'env', [list])
    app.add_directive_to_domain('c', 'autodoc', CAutoDocDirective)
    app.add_directive_to_domain('c', 'autovar', CAutoVarDirective)
    app.add_directive_to_domain('c', 'autotype', CAutoTypeDirective)
    app.add_directive_to_domain('c', 'autostruct', CAutoStructDirective)
    app.add_directive_to_domain('c', 'autounion', CAutoUnionDirective)
    app.add_directive_to_domain('c', 'autoenum', CAutoEnumDirective)
    app.add_directive_to_domain('c', 'automacro', CAutoMacroDirective)
    app.add_directive_to_domain('c', 'autofunction', CAutoFunctionDirective)

    return dict(version=__version__,
                parallel_read_safe=True, parallel_write_safe=True)
