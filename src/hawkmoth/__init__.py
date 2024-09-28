# Copyright (c) 2016-2017, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Hawkmoth
========

Sphinx C Domain autodoc directive extension.
"""

import glob
import os
from typing import Optional

from docutils import nodes
from docutils.parsers.rst import directives
from docutils.statemachine import ViewList
from sphinx import addnodes
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

    _domain: Optional[str] = None
    _docstring_types: Optional[list[type[docstring.Docstring]]] = None

    def __display_parser_diagnostics(self, errors):
        # Map parser diagnostic level to Sphinx level name
        log_level_map = {
            ErrorLevel.DEBUG: 'DEBUG',
            ErrorLevel.INFO: 'VERBOSE',
            ErrorLevel.WARNING: 'WARNING',
            ErrorLevel.ERROR: 'ERROR',
            ErrorLevel.CRITICAL: 'ERROR',
        }

        for error in errors:
            self.logger.log(log_level_map[error.level], error.get_message(),
                            location=(self.env.docname, self.lineno))

    def __get_clang_args(self):
        clang_args = []

        clang_args.extend(self.env.config.hawkmoth_clang.copy())

        if self._domain == 'c':
            clang_args.extend(self.env.config.hawkmoth_clang_c.copy())
        else:
            clang_args.extend(self.env.config.hawkmoth_clang_cpp.copy())

        clang_args.extend(self.options.get('clang', []))

        return clang_args

    def __parse(self, filename):
        clang_args = self.__get_clang_args()

        # Cached parse results per rst document
        parsed_files = self.env.temp_data.setdefault('hawkmoth_parsed_files', {})

        # The output depends on domain and clang args
        key = (filename, self._domain, tuple(clang_args))

        if key in parsed_files:
            return

        # Tell Sphinx about the dependency
        self.env.note_dependency(filename)

        docstrings, errors = parse(filename, domain=self._domain,
                                   clang_args=clang_args)

        self.__display_parser_diagnostics(errors)

        parsed_files[key] = docstrings

    def __parsed_files(self, filter_filenames=None, filter_domains=None,
                       filter_clang_args=None):
        parsed_files = self.env.temp_data.get('hawkmoth_parsed_files', {})

        for root in parsed_files.values():
            if filter_filenames is not None and root.get_filename() not in filter_filenames:
                continue

            if filter_domains is not None and root.get_domain() not in filter_domains:
                continue

            if filter_clang_args is not None and root.get_clang_args() not in filter_clang_args:
                continue

            yield root

    def __process_docstring(self, lines):
        transform = self.options.get('transform', self.env.config.hawkmoth_transform_default)

        self.env.app.emit('hawkmoth-process-docstring', lines, transform, self.options)

    def __get_docstrings_for_root(self, viewlist, root):
        def process_docstring(lines): self.__process_docstring(lines)

        num_matches = 0
        for docstrings in root.walk(recurse=False, filter_types=self._docstring_types,
                                    filter_names=self._get_names()):
            num_matches += 1
            for docstr in docstrings.walk(filter_names=self._get_members()):
                lines, line_number = docstr.get_docstring(process_docstring=process_docstring)
                for line in lines:
                    # viewlist line numbers are 0-based
                    viewlist.append(line, root.get_filename(), line_number - 1)
                    line_number += 1

        return num_matches

    def __get_docstrings(self, viewlist):
        num_matches = 0
        for root in self.__parsed_files(filter_filenames=self._get_filenames(),
                                        filter_domains=[self._domain],
                                        filter_clang_args=[self.__get_clang_args()]):
            num_matches += self.__get_docstrings_for_root(viewlist, root)

        if num_matches == 0:
            if self._get_names():
                args = ' '.join(self.arguments)
                self.logger.warning(f'"{self.name}:: {args}" does not match documented symbols.',
                                    location=(self.env.docname, self.lineno))
            else:
                # autodoc
                self.logger.warning('No documented symbols were found.',
                                    location=(self.env.docname, self.lineno))
        elif num_matches > 1 and self._get_names():
            args = ' '.join(self.arguments)
            self.logger.warning(f'"{self.name}:: {args}" matches {num_matches} documented symbols.',
                                location=(self.env.docname, self.lineno))

    def _get_names(self):
        return None

    def _get_members(self):
        return None

    def _get_filenames(self):
        raise NotImplementedError(self.__class__.__name__ + '._get_filenames')

    def run(self):
        if self._get_filenames():
            for filename in self._get_filenames():
                self.__parse(filename)

        result = ViewList()

        self.__get_docstrings(result)

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
        ret = []
        for pattern in self.arguments:
            filenames = glob.glob(os.path.join(self.env.config.hawkmoth_root, pattern))
            if len(filenames) == 0:
                self.logger.warning(f'Pattern "{pattern}" does not match any files.',
                                    location=(self.env.docname, self.lineno))
                continue

            for filename in filenames:
                if os.path.isfile(filename):
                    ret.append(os.path.abspath(filename))
                else:
                    self.logger.warning(f'Path "{filename}" matching pattern "{pattern}" is not a file.',  # noqa: E501
                                        location=(self.env.docname, self.lineno))

        return ret

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
        if not filename:
            return None

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

class CAutoSectionDirective(_AutoSymbolDirective):
    # Allow spaces in the directive argument (the name)
    final_argument_whitespace = True
    _domain = 'c'
    _docstring_types = [docstring.TextDocstring]

class CAutoVarDirective(_AutoSymbolDirective):
    _domain = 'c'
    _docstring_types = [docstring.VarDocstring]

class CAutoTypeDirective(_AutoSymbolDirective):
    _domain = 'c'
    _docstring_types = [docstring.TypedefDocstring]

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

class CppAutoSectionDirective(_AutoSymbolDirective):
    # Allow spaces in the directive argument (the name)
    final_argument_whitespace = True
    _domain = 'cpp'
    _docstring_types = [docstring.TextDocstring]

class CppAutoVarDirective(_AutoSymbolDirective):
    _domain = 'cpp'
    _docstring_types = [docstring.VarDocstring]

class CppAutoTypeDirective(_AutoSymbolDirective):
    _domain = 'cpp'
    _docstring_types = [docstring.TypedefDocstring, docstring.TypeAliasDocstring]

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

def _uri_format(env, signode):
    """Generate a source URI for signode"""
    uri_template = env.config.hawkmoth_source_uri

    if signode.source is None or signode.line is None:
        return None

    source = os.path.relpath(signode.source, start=env.config.hawkmoth_root)

    # Note: magic +1 to take into account we've added signode ourselves and its
    # not present in source
    uri = uri_template.format(source=source, line=signode.line + 1)

    return uri

def _doctree_read(app, doctree):
    env = app.builder.env

    # Bail out early if not configured
    uri_template = env.config.hawkmoth_source_uri
    if uri_template is None:
        return

    for objnode in list(doctree.findall(addnodes.desc)):
        if objnode.get('domain') not in ['c', 'cpp']:
            continue

        for signode in objnode:
            if not isinstance(signode, addnodes.desc_signature):
                continue

            uri = _uri_format(env, signode)
            if not uri:
                continue

            # Similar to sphinx.ext.linkcode
            inline = nodes.inline('', '[source]', classes=['viewcode-link'])
            onlynode = addnodes.only(expr='html')
            onlynode += nodes.reference('', '', inline, internal=False, refuri=uri)
            signode += onlynode

def setup(app):
    app.require_sphinx('3.0')

    app.add_config_value('hawkmoth_root', app.confdir, 'env', [str])
    app.add_config_value('hawkmoth_clang', [], 'env', [list])
    app.add_config_value('hawkmoth_clang_c', [], 'env', [list])
    app.add_config_value('hawkmoth_clang_cpp', [], 'env', [list])

    app.add_config_value('hawkmoth_transform_default', None, 'env', [str])

    app.add_directive_to_domain('c', 'autodoc', CAutoDocDirective)
    app.add_directive_to_domain('c', 'autosection', CAutoSectionDirective)
    app.add_directive_to_domain('c', 'autovar', CAutoVarDirective)
    app.add_directive_to_domain('c', 'autotype', CAutoTypeDirective)
    app.add_directive_to_domain('c', 'autostruct', CAutoStructDirective)
    app.add_directive_to_domain('c', 'autounion', CAutoUnionDirective)
    app.add_directive_to_domain('c', 'autoenum', CAutoEnumDirective)
    app.add_directive_to_domain('c', 'automacro', CAutoMacroDirective)
    app.add_directive_to_domain('c', 'autofunction', CAutoFunctionDirective)

    app.add_directive_to_domain('cpp', 'autodoc', CppAutoDocDirective)
    app.add_directive_to_domain('cpp', 'autosection', CppAutoSectionDirective)
    app.add_directive_to_domain('cpp', 'autovar', CppAutoVarDirective)
    app.add_directive_to_domain('cpp', 'autotype', CppAutoTypeDirective)
    app.add_directive_to_domain('cpp', 'autostruct', CppAutoStructDirective)
    app.add_directive_to_domain('cpp', 'autounion', CppAutoUnionDirective)
    app.add_directive_to_domain('cpp', 'autoenum', CppAutoEnumDirective)
    app.add_directive_to_domain('cpp', 'automacro', CppAutoMacroDirective)
    app.add_directive_to_domain('cpp', 'autofunction', CppAutoFunctionDirective)
    app.add_directive_to_domain('cpp', 'autoclass', CppAutoClassDirective)

    app.add_event('hawkmoth-process-docstring')

    # Source code link
    app.add_config_value('hawkmoth_source_uri', None, 'env', [str])
    app.connect('doctree-read', _doctree_read)

    return dict(version=__version__,
                parallel_read_safe=True, parallel_write_safe=True)
