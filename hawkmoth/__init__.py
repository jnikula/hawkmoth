# Copyright (c) 2016-2017, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Hawkmoth
========

Sphinx C Domain autodoc directive extension.
"""

import glob
import os

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from sphinx.util.nodes import nested_parse_with_titles
from sphinx.util.docutils import switch_source_input, SphinxDirective
from sphinx.util import logging

from hawkmoth.parser import parse, ErrorLevel
from hawkmoth.util import strutil
from hawkmoth import docstring

with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                       'VERSION')) as version_file:
    __version__ = version_file.read().strip()

class _AutoBaseDirective(SphinxDirective):
    logger = logging.getLogger(__name__)

    option_spec = {
        'transform': directives.unchanged_required,
        'clang': strutil.string_list,
    }
    has_content = False

    _domain = None
    _docstring_types = None

    def __display_parser_diagnostics(self, errors):
        # Map parser diagnostic level to Sphinx level name
        log_level_map = {
            ErrorLevel.DEBUG: 'DEBUG',
            ErrorLevel.INFO: 'VERBOSE',
            ErrorLevel.WARNING: 'WARNING',
            ErrorLevel.ERROR: 'ERROR',
            ErrorLevel.CRITICAL: 'CRITICAL',
        }

        for error in errors:
            self.logger.log(log_level_map[error.level], error.get_message(),
                            location=(self.env.docname, self.lineno))

    def __get_clang_args(self):
        clang_args = self.env.config.hawkmoth_clang.copy()

        clang_args.extend(self.options.get('clang', []))

        return clang_args

    def __parse(self, filename):
        # Always pass `-xc++` to the compiler on 'cpp' domain as the first
        # option so that the user can override it.
        clang_args = ['-xc++'] if self._domain == 'cpp' else []
        clang_args.extend(self.__get_clang_args())

        # Cached parse results per rst document
        parsed_files = self.env.temp_data.setdefault('cautodoc_parsed_files', {})

        # The output depends on clang args
        key = (filename, tuple(clang_args))

        if key in parsed_files:
            return parsed_files[key]

        # Tell Sphinx about the dependency
        self.env.note_dependency(filename)

        docstrings, errors = parse(filename, domain=self._domain,
                                   clang_args=clang_args)

        self.__display_parser_diagnostics(errors)

        parsed_files[key] = docstrings

        return docstrings

    def __process_docstring(self, lines):
        transform = self.options.get('transform', self.env.config.hawkmoth_transform_default)

        self.env.app.emit('hawkmoth-process-docstring', lines, transform, self.options)

    def __process_signature(self, lines):
        self.env.app.emit('hawkmoth-process-signature', lines, self.options)

    def __get_docstrings(self, viewlist, filename):
        root = self.__parse(filename)

        process_docstring = lambda lines: self.__process_docstring(lines)
        process_signature = lambda lines: self.__process_signature(lines)

        for docstrings in root.walk(recurse=False, filter_types=self._docstring_types,
                                    filter_names=self._get_names()):
            for docstr in docstrings.walk(filter_names=self._get_members()):
                lineoffset = docstr.get_line() - 1
                lines = docstr.get_docstring(transform=process_docstring,
                                             process_signature=process_signature)
                for line in lines:
                    viewlist.append(line, filename, lineoffset)
                    lineoffset += 1

    def _get_names(self):
        return None

    def _get_members(self):
        return None

    def _get_filenames(self):
        raise NotImplementedError(self.__class__.__name__ + '._get_filenames')

    def run(self):
        result = ViewList()

        for filename in self._get_filenames():
            self.__get_docstrings(result, filename)

        # Parse the extracted reST
        with switch_source_input(self.state, result):
            node = nodes.section()
            nested_parse_with_titles(self.state, result, node)

        return node.children

class _AutoDocDirective(_AutoBaseDirective):
    """Extract all documentation comments from the specified files"""

    # Allow passing a variable number of file patterns as arguments
    required_arguments = 1
    optional_arguments = 100   # arbitrary limit

    def _get_filenames(self):
        for pattern in self.arguments:
            filenames = glob.glob(os.path.join(self.env.config.hawkmoth_root, pattern))
            if len(filenames) == 0:
                self.logger.warning(f'Pattern "{pattern}" does not match any files.',
                                    location=(self.env.docname, self.lineno))
                continue

            for filename in filenames:
                if os.path.isfile(filename):
                    yield os.path.abspath(filename)
                else:
                    self.logger.warning(f'Path "{filename}" matching pattern "{pattern}" is not a file.',  # noqa: E501
                                        location=(self.env.docname, self.lineno))

# Base class for named stuff
class _AutoSymbolDirective(_AutoBaseDirective):
    """Extract specified documentation comments from the specified file"""

    required_arguments = 1
    optional_arguments = 0

    option_spec = _AutoBaseDirective.option_spec.copy()
    option_spec.update({
        'file': directives.unchanged_required,
    })

    def _get_filenames(self):
        filename = self.options.get('file')

        # Note: For the time being the file option is mandatory (sic).
        if not filename:
            self.logger.warning(':file: option missing.',
                                location=(self.env.docname, self.lineno))
            return []

        return [os.path.abspath(os.path.join(self.env.config.hawkmoth_root, filename))]

    def _get_names(self):
        return [self.arguments[0]]

def _members_filter(argument):
    # Use None for members option without an argument to not filter.
    if argument is None:
        return None
    return strutil.string_list(argument)

class _AutoCompoundDirective(_AutoSymbolDirective):
    option_spec = _AutoSymbolDirective.option_spec.copy()
    option_spec.update({
        'members': _members_filter,
    })

    def _get_members(self):
        # By default use [] as a filter that does not match any members.
        return self.options.get('members', [])

class CAutoDocDirective(_AutoDocDirective):
    _domain = 'c'

class CAutoVarDirective(_AutoSymbolDirective):
    _domain = 'c'
    _docstring_types = [docstring.VarDocstring]

class CAutoTypeDirective(_AutoSymbolDirective):
    _domain = 'c'
    _docstring_types = [docstring.TypeDocstring]

class CAutoMacroDirective(_AutoSymbolDirective):
    _domain = 'c'
    _docstring_types = [docstring.MacroDocstring, docstring.MacroFunctionDocstring]

class CAutoFunctionDirective(_AutoSymbolDirective):
    _domain = 'c'
    _docstring_types = [docstring.FunctionDocstring]

class CAutoStructDirective(_AutoCompoundDirective):
    _domain = 'c'
    _docstring_types = [docstring.StructDocstring]

class CAutoUnionDirective(_AutoCompoundDirective):
    _domain = 'c'
    _docstring_types = [docstring.UnionDocstring]

class CAutoEnumDirective(_AutoCompoundDirective):
    _domain = 'c'
    _docstring_types = [docstring.EnumDocstring]

class CppAutoDocDirective(_AutoDocDirective):
    _domain = 'cpp'

class CppAutoVarDirective(_AutoSymbolDirective):
    _domain = 'cpp'
    _docstring_types = [docstring.VarDocstring]

class CppAutoTypeDirective(_AutoSymbolDirective):
    _domain = 'cpp'
    _docstring_types = [docstring.TypeDocstring]

class CppAutoMacroDirective(_AutoSymbolDirective):
    _domain = 'cpp'
    _docstring_types = [docstring.MacroDocstring, docstring.MacroFunctionDocstring]

class CppAutoFunctionDirective(_AutoSymbolDirective):
    _domain = 'cpp'
    _docstring_types = [docstring.FunctionDocstring]

class CppAutoStructDirective(_AutoCompoundDirective):
    _domain = 'cpp'
    _docstring_types = [docstring.StructDocstring]

class CppAutoUnionDirective(_AutoCompoundDirective):
    _domain = 'cpp'
    _docstring_types = [docstring.UnionDocstring]

class CppAutoEnumDirective(_AutoCompoundDirective):
    _domain = 'cpp'
    _docstring_types = [docstring.EnumDocstring]

class CppAutoClassDirective(_AutoCompoundDirective):
    _domain = 'cpp'
    _docstring_types = [docstring.ClassDocstring]

def _deprecate(conf, old, new, default=None):
    if conf[old]:
        logger = logging.getLogger(__name__)
        logger.warning(f'{old} is deprecated in favour of {new}')
        conf[new] = conf[old]
        del conf[old]
        return conf[new]
    return default

def setup(app):
    app.require_sphinx('3.0')

    app.add_config_value('cautodoc_root', None, 'env', [str])
    app.add_config_value('cautodoc_clang', None, 'env', [list])

    app.add_config_value(
        'hawkmoth_root',
        lambda conf: _deprecate(conf, 'cautodoc_root', 'hawkmoth_root', app.confdir),
        'env', [str]
    )
    app.add_config_value(
        'hawkmoth_clang',
        lambda conf: _deprecate(conf, 'cautodoc_clang', 'hawkmoth_clang', []),
        'env', [list]
    )

    app.add_config_value('hawkmoth_transform_default', None, 'env', [str])

    app.add_directive_to_domain('c', 'autodoc', CAutoDocDirective)
    app.add_directive_to_domain('c', 'autovar', CAutoVarDirective)
    app.add_directive_to_domain('c', 'autotype', CAutoTypeDirective)
    app.add_directive_to_domain('c', 'autostruct', CAutoStructDirective)
    app.add_directive_to_domain('c', 'autounion', CAutoUnionDirective)
    app.add_directive_to_domain('c', 'autoenum', CAutoEnumDirective)
    app.add_directive_to_domain('c', 'automacro', CAutoMacroDirective)
    app.add_directive_to_domain('c', 'autofunction', CAutoFunctionDirective)

    app.add_directive_to_domain('cpp', 'autodoc', CppAutoDocDirective)
    app.add_directive_to_domain('cpp', 'autovar', CppAutoVarDirective)
    app.add_directive_to_domain('cpp', 'autotype', CppAutoTypeDirective)
    app.add_directive_to_domain('cpp', 'autostruct', CppAutoStructDirective)
    app.add_directive_to_domain('cpp', 'autounion', CppAutoUnionDirective)
    app.add_directive_to_domain('cpp', 'autoenum', CppAutoEnumDirective)
    app.add_directive_to_domain('cpp', 'automacro', CppAutoMacroDirective)
    app.add_directive_to_domain('cpp', 'autofunction', CppAutoFunctionDirective)
    app.add_directive_to_domain('cpp', 'autoclass', CppAutoClassDirective)

    app.add_event('hawkmoth-process-docstring')
    app.add_event('hawkmoth-process-signature')

    # Setup transformations for compatibility.
    app.setup_extension('hawkmoth.ext.transformations')

    return dict(version=__version__,
                parallel_read_safe=True, parallel_write_safe=True)
