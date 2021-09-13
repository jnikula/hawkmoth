#!/usr/bin/env python3
# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os

import pytest

from hawkmoth.parser import parse
from hawkmoth.util import doccompat
from test import conf, testenv

def _get_output(testcase, **options):
    docs_str = ''
    errors_str = ''

    directive = options.get('directive')
    if directive:
        pytest.skip(f'{directive} directive test')

    input_filename = testenv.get_input_filename(options, path=testenv.testdir)

    options = options.get('directive-options', {})

    clang_args = options.get('clang')
    comments, errors = parse(input_filename, clang_args=clang_args)

    tropt = options.pop('compat', None)
    if tropt is not None:
        transform = lambda comment: doccompat.convert(comment, transform=tropt)
    else:
        tropt = options.pop('transform', None)
        if tropt is not None:
            transform = conf.cautodoc_transformations[tropt]
        else:
            transform = None

    for comment in comments.walk():
        docs_str += comment.get_docstring(transform=transform) + '\n'

    for (severity, filename, lineno, msg) in errors:
        errors_str += f'{severity.name}: {os.path.basename(filename)}:{lineno}: {msg}\n'

    return docs_str, errors_str

def _get_expected(testcase, **options):
    return testenv.read_file(testcase, ext='rst'), \
        testenv.read_file(testcase, ext='stderr')

@pytest.mark.parametrize('testcase', testenv.get_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_parser(testcase):
    testenv.run_test(testcase, _get_output, _get_expected)
