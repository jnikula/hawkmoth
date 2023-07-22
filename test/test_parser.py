#!/usr/bin/env python3
# Copyright (c) 2018-2023, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os

from sphinx.ext import napoleon
import pytest

from hawkmoth import docstring
from hawkmoth.parser import parse
from hawkmoth.util import doccompat
from test import testenv

def napoleon_transform(comment):
    config = napoleon.Config(napoleon_use_rtype=False)
    return str(napoleon.docstring.GoogleDocstring(comment, config))

parser_transformations = {
    'napoleon': napoleon_transform,
    'javadoc': doccompat.javadoc_liberal,
}

def _process_docstring(transform, lines):
    if transform:
        text = '\n'.join(lines)
        text = transform(text)
        lines[:] = [line for line in text.splitlines()]

def _filter_types(directive):
    types = {
        'autodoc': None,
        'autosection': [docstring.TextDocstring],
        'autovar': [docstring.VarDocstring],
        'autotype': [docstring.TypeDocstring],
        'autostruct': [docstring.StructDocstring],
        'autounion': [docstring.UnionDocstring],
        'autoenum': [docstring.EnumDocstring],
        'automacro': [docstring.MacroDocstring, docstring.MacroFunctionDocstring],
        'autofunction': [docstring.FunctionDocstring],
        'autoclass': [docstring.ClassDocstring],
    }

    return types.get(directive)

def _filter_names(directive):
    if directive.directive == 'autodoc':
        return None

    return directive.arguments

def _filter_members(directive):
    if directive.directive in ['autodoc', 'autotext', 'autovar', 'autotype',
                               'automacro', 'autofunction']:
        return None

    members = directive.options.get('members')

    if members is None:
        return []

    if len(members) == 0:
        return None

    return members

class ParserTestcase(testenv.Testcase):
    def get_output(self):
        roots = {}
        docs_str = ''
        errors_str = ''

        for directive in self.directives:
            filename = directive.get_input_filename()
            if not filename:
                continue

            clang_args = directive.get_clang_args()

            key = (filename, tuple(clang_args))
            if key in roots:
                continue

            root, errors = parse(filename, domain=directive.domain, clang_args=clang_args)

            roots[key] = root

            for error in errors:
                errors_str += f'{error.level.name}: {os.path.basename(error.filename)}:{error.line}: {error.message}\n'  # noqa: E501

        for directive in self.directives:
            filename = directive.get_input_filename()
            filter_filenames = [filename] if filename is not None else None
            filter_clang_args = [directive.get_clang_args()]

            for root in roots.values():
                if filter_filenames is not None and root.get_filename() not in filter_filenames:
                    continue

                if filter_clang_args is not None and root.get_clang_args() not in filter_clang_args:
                    continue

                tropt = directive.options.get('transform')
                if tropt is not None:
                    transform = parser_transformations[tropt]
                else:
                    transform = None

                process_docstring = lambda lines: _process_docstring(transform, lines)

                for docstrings in root.walk(recurse=False, filter_types=_filter_types(directive),
                                            filter_names=_filter_names(directive)):
                    for docstr in docstrings.walk(filter_names=_filter_members(directive)):
                        lines = docstr.get_docstring(process_docstring=process_docstring)
                        docs_str += '\n'.join(lines) + '\n'

        return docs_str, errors_str

    def get_expected(self):
        return testenv.read_file(self.get_expected_filename()), \
            testenv.read_file(self.get_stderr_filename(), optional=True)

def _get_parser_testcases(path):
    for f in testenv.get_testcase_filenames(path):
        yield ParserTestcase(f)

@pytest.mark.parametrize('testcase', _get_parser_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_parser(testcase):
    testcase.run_test()
