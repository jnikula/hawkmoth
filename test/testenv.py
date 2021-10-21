# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import sys

import pytest
import strictyaml

testext = '.yaml'
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
    strictyaml.Optional('directive-arguments'): strictyaml.Seq(strictyaml.Str()),
    strictyaml.Optional('directive-options'): strictyaml.Map({
        strictyaml.Optional('clang'): strictyaml.Seq(strictyaml.Str()),
        strictyaml.Optional('compat'): strictyaml.Str(),
        strictyaml.Optional('file'): strictyaml.Str(),
        strictyaml.Optional('members'): strictyaml.Seq(strictyaml.Str()) | strictyaml.EmptyList(),
        strictyaml.Optional('transform'): strictyaml.Str(),
    }),
    strictyaml.Optional('expected-failure'): strictyaml.Bool(),
})

def get_testcase_options(testcase):
    # options are optional
    options = {}
    if os.path.isfile(testcase):
        with open(testcase, 'r') as f:
            options = strictyaml.load(f.read(), options_schema).data

    return options

def get_input_filename(options, path=None):
    directive = options.get('directive', 'autodoc')
    if directive == 'autodoc':
        arguments = options.get('directive-arguments', [])
        basename = arguments[0]
    else:
        directive_options = options.get('directive-options', {})
        basename = directive_options.get('file')

    if path:
        return os.path.join(path, basename)
    else:
        return basename

def get_directive_string(options):
    directive = options.get('directive', 'autodoc')
    arguments = options.get('directive-arguments', [])
    arguments_str = ' '.join(arguments)

    directive_str = f'.. c:{directive}:: {arguments_str}\n'

    directive_options = options.get('directive-options', {})

    for key, value in directive_options.items():
        if isinstance(value, list):
            value = ', '.join(value)
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

def run_test(testcase, get_output, get_expected, monkeypatch=None, capsys=None):
    options = get_testcase_options(testcase)

    if options.get('expected-failure'):
        pytest.xfail()

    output_docs, output_errors = get_output(testcase, monkeypatch=monkeypatch,
                                            capsys=capsys, **options)
    expect_docs, expect_errors = get_expected(testcase, monkeypatch=monkeypatch,
                                              capsys=capsys, **options)

    assert output_docs == expect_docs
    assert output_errors == expect_errors
