#!/usr/bin/env python3
# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os

import pytest

from hawkmoth.parser import parse
from test import conf, testenv

def _transform(transform, lines):
    if transform:
        text = '\n'.join(lines)
        text = transform(text)
        lines[:] = [line for line in text.splitlines()]

def _get_output(testcase, **options):
    docs_str = ''
    errors_str = ''

    domain = options.get('domain')

    # Default to compile as C++ if the test is for the C++ domain so that we can
    # use C sources for C++ tests. The yaml may override this in cases where we
    # want to force a mismatch.
    clang_args = ['-xc++'] if domain == 'cpp' else ['-xc']

    directive = options.get('directive')
    if directive != 'autodoc':
        pytest.skip(f'{directive} directive test')

    input_filename = testcase.get_input_filename()

    options = options.get('directive-options', {})

    clang_args.extend(options.get('clang', []))
    comments, errors = parse(input_filename, domain=domain, clang_args=clang_args)

    tropt = options.pop('transform', None)
    if tropt is not None:
        transform = conf.cautodoc_transformations[tropt]
    else:
        transform = None

    for comment in comments.walk():
        lines = comment.get_docstring(transform=lambda lines: _transform(transform, lines))
        docs_str += '\n'.join(lines) + '\n'

    for error in errors:
        errors_str += f'{error.level.name}: {os.path.basename(error.filename)}:{error.line}: {error.message}\n'  # noqa: E501

    return docs_str, errors_str

def _get_expected(testcase, **options):
    return testenv.read_file(testenv.get_expected_filename(testcase)), \
        testenv.read_file(testenv.get_stderr_filename(testcase))

@pytest.mark.parametrize('testcase', testenv.get_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_parser(testcase):
    testenv.run_test(testcase, _get_output, _get_expected)
