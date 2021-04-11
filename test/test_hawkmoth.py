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

    transform = options.pop('compat', None)
    if transform is not None:
        options['transform'] = lambda comment: doccompat.convert(comment, transform=transform)
    else:
        transform = options.pop('transform', None)
        if transform is not None:
            options['transform'] = conf.cautodoc_transformations[transform]

    docs, errors = parse(input_filename, **options)

    for (doc, meta) in docs:
        docs_str += doc + '\n'

    for (severity, filename, lineno, msg) in errors:
        errors_str += f'{severity.name}: {lineno}: {msg}\n'

    return docs_str, errors_str

def _get_expected(input_filename, **options):
    return testenv.read_file(input_filename, ext='rst'), \
        testenv.read_file(input_filename, ext='stderr')

@pytest.mark.parametrize('input_filename', testenv.get_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_parser(input_filename):
    testenv.run_test(input_filename, _get_output, _get_expected)

