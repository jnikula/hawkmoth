#!/usr/bin/env python3
# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os

import pytest

from hawkmoth.parser import parse
from hawkmoth.util import doccompat
from test import conf, testenv

def _get_output(input_filename, **options):
    docs_str = ''
    errors_str = ''

    directive = options.get('directive')
    if directive:
        pytest.skip(f'{directive} directive test')

    options = options.get('directive-options', {})

    tropt = options.pop('compat', None)
    if tropt is not None:
        transform = lambda comment: doccompat.convert(comment, transform=tropt)
    else:
        tropt = options.pop('transform', None)
        if tropt is not None:
            transform = conf.cautodoc_transformations[tropt]
        else:
            transform = None

    comments, errors = parse(input_filename, **options)

    for comment in comments.recursive_walk():
        docs_str += comment.get_docstring(transform=transform) + '\n'

    for (severity, filename, lineno, msg) in errors:
        errors_str += f'{severity.name}: {os.path.basename(filename)}:{lineno}: {msg}\n'

    return docs_str, errors_str

def _get_expected(input_filename, **options):
    return testenv.read_file(input_filename, ext='rst'), \
        testenv.read_file(input_filename, ext='stderr')

@pytest.mark.parametrize('input_filename', testenv.get_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_parser(input_filename):
    testenv.run_test(input_filename, _get_output, _get_expected)

