#!/usr/bin/env python3
# Copyright (c) 2018-2023, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os

import pytest

from hawkmoth.parser import parse
from hawkmoth import docstring
from test import conf, testenv

def _transform(transform, lines):
    if transform:
        text = '\n'.join(lines)
        text = transform(text)
        lines[:] = [line for line in text.splitlines()]

def _filter_types(directive):
    types = {
        'autodoc': None,
        'autotext': [docstring.TextDocstring],
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

def _filter_names(directive, options):
    if directive == 'autodoc':
        return None

    return options.get('directive-arguments')

def _filter_members(directive, directive_options):
    if directive in ['autodoc', 'autotext', 'autovar', 'autotype', 'automacro', 'autofunction']:
        return None

    members = directive_options.get('members')

    if members is None:
        return []

    if len(members) == 0:
        return None

    return members

class ParserTestcase(testenv.Testcase):
    def get_output(self):
        options = self.options

        docs_str = ''
        errors_str = ''

        domain = options.get('domain')

        # Default to compile as C++ if the test is for the C++ domain so that we can
        # use C sources for C++ tests. The yaml may override this in cases where we
        # want to force a mismatch.
        clang_args = ['-xc++'] if domain == 'cpp' else ['-xc']

        directive = options.get('directive')

        input_filename = self.get_input_filename()

        directive_options = options.get('directive-options', {})

        clang_args.extend(directive_options.get('clang', []))
        root, errors = parse(input_filename, domain=domain, clang_args=clang_args)

        tropt = directive_options.get('transform')
        if tropt is not None:
            transform = conf.cautodoc_transformations[tropt]
        else:
            transform = None

        for docstrings in root.walk(recurse=False, filter_types=_filter_types(directive),
                                    filter_names=_filter_names(directive, options)):
            for docstr in docstrings.walk(filter_names=_filter_members(directive, directive_options)):  # noqa: E501
                lines = docstr.get_docstring(transform=lambda lines: _transform(transform, lines))
                docs_str += '\n'.join(lines) + '\n'

        for error in errors:
            errors_str += f'{error.level.name}: {os.path.basename(error.filename)}:{error.line}: {error.message}\n'  # noqa: E501

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
