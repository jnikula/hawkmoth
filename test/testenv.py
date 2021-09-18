# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import sys

import pytest
import strictyaml

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

options_schema = strictyaml.Map({
    strictyaml.Optional('directive'): strictyaml.Str(),
    strictyaml.Optional('directive-arguments'): strictyaml.Str(),
    strictyaml.Optional('directive-options'): strictyaml.Map({
        strictyaml.Optional('clang'): strictyaml.Seq(strictyaml.Str()),
        strictyaml.Optional('compat'): strictyaml.Str(),
        strictyaml.Optional('file'): strictyaml.Str(),
        strictyaml.Optional('members'): strictyaml.Str(),
        strictyaml.Optional('transform'): strictyaml.Str(),
    }),
    strictyaml.Optional('expected-failure'): strictyaml.Bool(),
})

def get_testcase_options(testcase):
    options_filename = modify_filename(testcase, ext='yaml')

    # options are optional
    options = {}
    if os.path.isfile(options_filename):
        with open(options_filename, 'r') as f:
            options = strictyaml.load(f.read(), options_schema).data

    return options

def get_directive_string(options, filename):
    directive = options.get('directive')
    if directive:
        arguments = options.get('directive-arguments', '')
        sep = ' ' if arguments else ''
        directive_str = f'.. c:{directive}::{sep}{arguments}\n'
    else:
        directive_str = f'.. c:autodoc:: {filename}\n'

    directive_options = options.get('directive-options', {})

    for key, value in directive_options.items():
        if isinstance(value, list):
            value = ', '.join(value)
        elif key == 'file' and value == '':
            # Special case to avoid lots of duplication.
            value = filename
        directive_str += f'   :{key}: {value}\n'

    return directive_str

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

def run_test(input_filename, get_output, get_expected, monkeypatch=None, capsys=None):
    options = get_testcase_options(input_filename)

    if options.get('expected-failure'):
        pytest.xfail()

    output_docs, output_errors = get_output(input_filename, monkeypatch=monkeypatch, capsys=capsys, **options)
    expect_docs, expect_errors = get_expected(input_filename, monkeypatch=monkeypatch, capsys=capsys, **options)

    assert expect_docs == output_docs
    assert expect_errors == output_errors
