#!/usr/bin/env python3
# Copyright (c) 2021, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import re

import pytest

from hawkmoth.__main__ import main
from test import testenv

# Replace full filename in a stderr line with basename
def _basename(line):
    mo = re.match(r'(?P<severity>[^:]+): (?P<filename>[^:]+):(?P<lineno>[^:]+):(?P<msg>.*)', line)
    if mo is None:
        return line

    severity = mo.group('severity')
    filename = mo.group('filename')
    lineno = mo.group('lineno')
    msg = mo.group('msg')

    return f'{severity}: {os.path.basename(filename)}:{lineno}:{msg}'

# Replace full filenames in stderr with basenames
def _stderr_basename(errors_str):
    if errors_str:
        errors_str = '\n'.join([_basename(line) for line in errors_str.splitlines()]) + '\n'

    return errors_str


class CliTestcase(testenv.Testcase):
    def set_monkeypatch(self, monkeypatch):
        self.monkeypatch = monkeypatch
        self.mock_args([])

    # Mock sys.argv for cli
    def mock_args(self, args):
        self.monkeypatch.setattr('sys.argv', ['dummy'] + args)

    def set_capsys(self, capsys):
        self.capsys = capsys

    # Capture stdout, stderr from cli
    def capture(self):
        captured = self.capsys.readouterr()

        return captured.out, _stderr_basename(captured.err)

    def get_output(self):
        options = self.options

        args = [self.get_input_filename()]

        directive = options.get('directive')
        if directive != 'autodoc':
            pytest.skip(f'{directive} directive test')

        domain = options.get('domain')
        if domain is not None:
            args += [f'--domain={domain}']
            args += [f'--clang={"-xc++" if domain == "cpp" else "-xc"}']

        directive_options = options.get('directive-options', {})

        transform = directive_options.get('transform')
        if transform is not None:
            pytest.skip('cli does not support generic transformations')

        clang_args = directive_options.get('clang')
        if clang_args:
            args += [f'--clang={clang_arg}' for clang_arg in clang_args]

        self.mock_args(args)

        main()

        docs_str, errors_str = self.capture()

        return docs_str, errors_str

    def get_expected(self):
        return testenv.read_file(self.get_expected_filename()), \
            testenv.read_file(self.get_stderr_filename())

def _get_cli_testcases(path):
    for f in testenv.get_testcase_filenames(path):
        yield CliTestcase(f)

@pytest.mark.full
@pytest.mark.parametrize('testcase', _get_cli_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_cli(testcase, monkeypatch, capsys):
    testcase.set_monkeypatch(monkeypatch)
    testcase.set_capsys(capsys)
    testcase.run_test()
