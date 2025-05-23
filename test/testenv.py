# SPDX-FileCopyrightText: 2018 Jani Nikula <jani@nikula.org>
# SPDX-FileCopyrightText: 2025 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
# SPDX-License-Identifier: BSD-2-Clause

import os
import sys

import pytest
import strictyaml

from hawkmoth.util import compiler
from test import conf

testext = '.yaml'
testdir = os.path.dirname(os.path.abspath(__file__))
rootdir = os.path.dirname(testdir)

sys.path.insert(0, rootdir)

class Directive:
    def __init__(self, testcase, directive_config):
        self.testcase = testcase

        self.domain = directive_config.get('domain')
        self.directive = directive_config.get('directive')
        self.arguments = directive_config.get('arguments', [])
        self.options = directive_config.get('options', {})

    def get_input_filename(self):
        if self.directive == 'autodoc':
            basename = self.arguments[0]
        else:
            basename = self.options.get('file')

        return self.testcase.get_relative_filename(basename)

    def get_directive_string(self):
        arguments_str = ' '.join(self.arguments)
        directive_str = f'.. {self.domain}:{self.directive}:: {arguments_str}\n'

        for key, value in self.options.items():
            if isinstance(value, list):
                value = ', '.join(value)
            space = ' ' if len(value) else ''
            directive_str += f'   :{key}:{space}{value}\n'

        return directive_str

    def get_clang_args(self):
        clang_args = getattr(conf, 'hawkmoth_clang', [])

        if self.domain == 'c':
            clang_args.extend(getattr(conf, 'hawkmoth_clang_c', []))
            clang_args.extend(self.options.get('clang', []))
            clang_args.extend(compiler.get_include_args('clang', 'c'))
        else:
            clang_args.extend(getattr(conf, 'hawkmoth_clang_cpp', []))
            clang_args.extend(self.options.get('clang', []))
            clang_args.extend(compiler.get_include_args('clang', 'c++'))

        return clang_args

class Testcase:
    _options_schema = strictyaml.Map({
        strictyaml.Optional('test'): strictyaml.Seq(strictyaml.Str()),
        'directives': strictyaml.Seq(strictyaml.Map({
            'domain': strictyaml.Enum(['c', 'cpp']),
            'directive': strictyaml.Str(),
            strictyaml.Optional('arguments'): strictyaml.Seq(strictyaml.Str()),
            strictyaml.Optional('options'): strictyaml.Map({
                strictyaml.Optional('clang'): strictyaml.Seq(strictyaml.Str()),
                strictyaml.Optional('file'): strictyaml.Str(),
                strictyaml.Optional('members'): (strictyaml.Seq(strictyaml.Str()) |
                                                 strictyaml.EmptyList()),
                strictyaml.Optional('transform'): strictyaml.Str(),
            }),
        })),
        strictyaml.Optional('conf-overrides'): strictyaml.MapPattern(
            strictyaml.Str(), strictyaml.NullNone() | strictyaml.EmptyList() | strictyaml.Any(),
        ),
        strictyaml.Optional('expected-failure'): strictyaml.Bool(),
        strictyaml.Optional('example-use-namespace'): strictyaml.Bool(),
        strictyaml.Optional('example-title'): strictyaml.Str(),
        strictyaml.Optional('example-priority'): strictyaml.Int(),
        strictyaml.Optional('errors'): strictyaml.Str(),
        'expected': strictyaml.Str(),
    })

    def __init__(self, filename):
        self.filename = filename
        with open(filename) as f:
            self.options = strictyaml.load(f.read(), self._options_schema).data
            if self.options.get('test', None) is None:
                self.options['test'] = ['cli', 'parser', 'extension']
        self.testid = os.path.splitext(os.path.relpath(self.filename, testdir))[0]

        self.directives = [Directive(self, directive_config) for
                           directive_config in self.options.get('directives')]

    def get_testid(self):
        return self.testid

    def get_relative_filename(self, relative):
        if relative is None:
            return None

        return os.path.join(os.path.dirname(self.filename), relative)

    def get_expected_filename(self):
        return self.get_relative_filename(self.options.get('expected'))

    def get_stderr_filename(self):
        return self.get_relative_filename(self.options.get('errors'))

    def get_conf_overrides(self):
        return self.options.get('conf-overrides', {})

    def run_test(self):
        if self.options.get('expected-failure'):
            pytest.xfail()

        output_docs, output_errors = self.get_output()
        expect_docs, expect_errors = self.get_expected()

        assert output_docs, 'empty output'
        assert expect_docs, 'empty expected'
        assert output_docs + output_errors == expect_docs + expect_errors

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

    with open(filename) as f:
        return f.read()
