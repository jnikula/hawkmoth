#!/usr/bin/env python3
# Copyright (c) 2021, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import re

import pytest

from hawkmoth.__main__ import main
from test import testenv

# Mock sys.argv for cli
def _mock_args(monkeypatch, args):
    monkeypatch.setattr('sys.argv', ['dummy'] + args)

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

# Capture stdout, stderr from cli
def _capture(capsys):
    captured = capsys.readouterr()

    return captured.out, _stderr_basename(captured.err)

def _get_output(testcase, monkeypatch, capsys, **options):
    args = [testcase.get_input_filename()]

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

    _mock_args(monkeypatch, args)

    main()

    docs_str, errors_str = _capture(capsys)

    return docs_str, errors_str

def _get_expected(testcase, monkeypatch, **options):
    return testenv.read_file(testcase.get_expected_filename()), \
        testenv.read_file(testenv.get_stderr_filename(testcase))

@pytest.mark.full
@pytest.mark.parametrize('testcase', testenv.get_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_cli(testcase, monkeypatch, capsys):
    monkeypatch.setattr('sys.argv', ['dummy'])
    testenv.run_test(testcase, _get_output, _get_expected, monkeypatch, capsys)
