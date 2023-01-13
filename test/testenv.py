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

options_schema = strictyaml.Map({
    'domain': strictyaml.Enum(['c', 'cpp']),
    'directive': strictyaml.Str(),
    strictyaml.Optional('directive-arguments'): strictyaml.Seq(strictyaml.Str()),
    strictyaml.Optional('directive-options'): strictyaml.Map({
        strictyaml.Optional('clang'): strictyaml.Seq(strictyaml.Str()),
        strictyaml.Optional('file'): strictyaml.Str(),
        strictyaml.Optional('members'): strictyaml.Seq(strictyaml.Str()) | strictyaml.EmptyList(),
        strictyaml.Optional('transform'): strictyaml.Str(),
    }),
    strictyaml.Optional('expected-failure'): strictyaml.Bool(),
    strictyaml.Optional('example-use-namespace'): strictyaml.Bool(),
    strictyaml.Optional('example-title'): strictyaml.Str(),
    strictyaml.Optional('example-priority'): strictyaml.Int(),
    strictyaml.Optional('errors'): strictyaml.Str(),
    'expected': strictyaml.Str(),
})

class Testcase:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as f:
            self.options = strictyaml.load(f.read(), options_schema).data

    def get_testid(self):
        """Convert a testcase filename into a test case identifier."""
        name = os.path.splitext(os.path.basename(self.filename))[0]

        return name

    def get_relative_filename(self, relative):
        if relative is None:
            return None

        return os.path.join(os.path.dirname(self.filename), relative)

    def get_input_filename(self):
        options = self.options

        directive = options.get('directive')
        if directive == 'autodoc':
            arguments = options.get('directive-arguments', [])
            basename = arguments[0]
        else:
            directive_options = options.get('directive-options', {})
            basename = directive_options.get('file')

        return self.get_relative_filename(basename)

    def get_expected_filename(self):
        return self.get_relative_filename(self.options.get('expected'))

def get_testid(testcase):
    return testcase.get_testid()

def get_testcase_options(testcase):
    return testcase.options

def get_testcase_filenames(path):
    for f in sorted(os.listdir(path)):
        if f.endswith(testext):
            yield os.path.join(path, f)

def get_testcases(path):
    for f in get_testcase_filenames(path):
        yield Testcase(f)

def get_stderr_filename(testcase):
    options = get_testcase_options(testcase)

    return testcase.get_relative_filename(options.get('errors'))

def get_directive_string(options):
    domain = options.get('domain', None)
    directive = options.get('directive')
    arguments = options.get('directive-arguments', [])
    arguments_str = ' '.join(arguments)

    directive_str = f'.. {domain}:{directive}:: {arguments_str}\n'

    directive_options = options.get('directive-options', {})

    for key, value in directive_options.items():
        if isinstance(value, list):
            value = ', '.join(value)
        space = ' ' if len(value) else ''
        directive_str += f'   :{key}:{space}{value}\n'

    return directive_str

def read_file(filename):
    if not filename or not os.path.isfile(filename):
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
