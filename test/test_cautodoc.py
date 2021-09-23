#!/usr/bin/env python3
# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import shutil

import pytest
from sphinx_testing import with_app

from test import testenv

def _get_output(input_filename, app, status, warning, output_suffix, **options):
    shutil.copyfile(input_filename,
                    testenv.modify_filename(input_filename, dir=app.srcdir))

    directive_str = testenv.get_directive_string(options)

    with open(os.path.join(app.srcdir, 'index.rst'), 'w') as f:
        f.write(directive_str)

    app.build()

    output_filename = os.path.join(app.outdir, f'index.{output_suffix}')

    return testenv.read_file(output_filename), None

def _get_expected(input_filename, app, status, warning, output_suffix, **options):
    shutil.copyfile(testenv.modify_filename(input_filename, ext='rst'),
                    os.path.join(app.srcdir, 'index.rst'))

    app.build()

    output_filename = os.path.join(app.outdir, f'index.{output_suffix}')

    return testenv.read_file(output_filename), None

# Test using Sphinx plain text builder
@with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='text')
def _get_output_text(input_filename, app, status, warning, **options):
    return _get_output(input_filename, app, status, warning, 'txt', **options)

@with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='text')
def _get_expected_text(input_filename, app, status, warning, **options):
    return _get_expected(input_filename, app, status, warning, 'txt', **options)

@pytest.mark.parametrize('input_filename', testenv.get_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_directive_text(input_filename):
    testenv.run_test(input_filename, _get_output_text, _get_expected_text)

# Test using Sphinx html builder
@with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='html')
def _get_output_html(input_filename, app, status, warning, **options):
    return _get_output(input_filename, app, status, warning, 'html', **options)

@with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='html')
def _get_expected_html(input_filename, app, status, warning, **options):
    return _get_expected(input_filename, app, status, warning, 'html', **options)

@pytest.mark.full
@pytest.mark.parametrize('input_filename', testenv.get_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_directive_html(input_filename):
    testenv.run_test(input_filename, _get_output_html, _get_expected_html)
