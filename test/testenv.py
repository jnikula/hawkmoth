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

class Testcase:
    _options_schema = strictyaml.Map({
        'domain': strictyaml.Enum(['c', 'cpp']),
        'directive': strictyaml.Str(),
        strictyaml.Optional('directive-arguments'): strictyaml.Seq(strictyaml.Str()),
        strictyaml.Optional('directive-options'): strictyaml.Map({
            strictyaml.Optional('clang'): strictyaml.Seq(strictyaml.Str()),
            strictyaml.Optional('file'): strictyaml.Str(),
            strictyaml.Optional('members'): (strictyaml.Seq(strictyaml.Str()) |
                                             strictyaml.EmptyList()),
            strictyaml.Optional('transform'): strictyaml.Str(),
        }),
        strictyaml.Optional('expected-failure'): strictyaml.Bool(),
        strictyaml.Optional('example-use-namespace'): strictyaml.Bool(),
        strictyaml.Optional('example-title'): strictyaml.Str(),
        strictyaml.Optional('example-priority'): strictyaml.Int(),
        strictyaml.Optional('errors'): strictyaml.Str(),
        'expected': strictyaml.Str(),
    })

    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as f:
            self.options = strictyaml.load(f.read(), self._options_schema).data
        self.testid = os.path.splitext(os.path.relpath(self.filename, testdir))[0]

    def get_testid(self):
        return self.testid

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

    def get_stderr_filename(self):
        return self.get_relative_filename(self.options.get('errors'))

    def get_directive_string(self):
        options = self.options

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

    def run_test(self):
        if self.options.get('expected-failure'):
            pytest.xfail()

        output_docs, output_errors = self.get_output()
        expect_docs, expect_errors = self.get_expected()

        assert output_docs, 'empty output'
        assert expect_docs, 'empty expected'
        assert output_docs == expect_docs
        assert output_errors == expect_errors

def get_testid(testcase):
    return testcase.get_testid()

def get_testcase_filenames(path):
    for root, dirs, files in sorted(os.walk(path)):
        for f in files:
            if f.endswith(testext):
                yield os.path.join(root, f)

def read_file(filename, optional=False):
    if not filename:
        assert optional

        # Emulate empty file.
        return ''

    assert os.path.isfile(filename)

    with open(filename, 'r') as f:
        return f.read()
