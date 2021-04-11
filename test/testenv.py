# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import sys

import pytest

testext = '.c'
testdir = os.path.dirname(os.path.abspath(__file__))
rootdir = os.path.dirname(testdir)

sys.path.insert(0, rootdir)

def get_testid(testcase):
    """Convert a testcase filename into a test case identifier."""
    name = os.path.splitext(os.path.basename(testcase))[0]

    return name

def get_testcases(path):
    for f in sorted(os.listdir(path)):
        if f.endswith(testext):
            yield os.path.join(path, f)

directive_options = [
    'compat',
    'clang',
    'transform',
]

def get_testcase_options(testcase):
    options_filename = modify_filename(testcase, ext='options')

    # options are optional
    options = {}
    if os.path.isfile(options_filename):
        with open(options_filename, 'r') as f:
            for line in f.readlines():
                opt = [x.strip() for x in line.split('=', 1)]
                if opt[0] != '':
                    if len(opt) == 2:
                        options[opt[0]] = opt[1]
                    else:
                        options[opt[0]] = True

    return options

def modify_filename(filename, **kwargs):
    ext = kwargs.get('ext')
    if ext is not None:
        base, extension = os.path.splitext(filename)
        filename = base + '.' + ext

    dirname = kwargs.get('dir')
    if dirname is not None:
        base = os.path.basename(filename)
        filename = os.path.join(dirname, base)

    return filename

def read_file(filename, **kwargs):
    filename = modify_filename(filename, **kwargs)

    if not os.path.isfile(filename):
        # Emulate empty file.
        return ''

    with open(filename, 'r') as f:
        return f.read()

def run_test(input_filename, get_output, get_expected):
    options = get_testcase_options(input_filename)

    if options.get('test-expected-failure') is not None:
        pytest.xfail()

    output_docs, output_errors = get_output(input_filename, **options)
    expect_docs, expect_errors = get_expected(input_filename, **options)

    assert expect_docs == output_docs
    assert expect_errors == output_errors
