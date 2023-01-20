#!/usr/bin/env python3
# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import shutil

import pytest
from sphinx_testing import with_app

from test import testenv

def _get_suffix(buildername):
    return 'txt' if buildername == 'text' else buildername

class ExtensionTestcase(testenv.Testcase):
    def get_output(self, app, status, warning):
        directive_str = self.get_directive_string()

        with open(os.path.join(app.srcdir, 'index.rst'), 'w') as f:
            f.write(directive_str)

        # Hack: It's not possible to disable search via configuration
        app.builder.search = False

        app.build()

        output_suffix = _get_suffix(app.builder.name)
        output_filename = os.path.join(app.outdir, f'index.{output_suffix}')

        return testenv.read_file(output_filename), None

    def get_expected(self, app, status, warning):
        shutil.copyfile(self.get_expected_filename(),
                        os.path.join(app.srcdir, 'index.rst'))

        # Hack: It's not possible to disable search via configuration
        app.builder.search = False

        app.build()

        output_suffix = _get_suffix(app.builder.name)
        output_filename = os.path.join(app.outdir, f'index.{output_suffix}')

        return testenv.read_file(output_filename), None

# Test using Sphinx plain text builder
class ExtensionTextTestcase(ExtensionTestcase):
    @with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='text')
    def get_output(self, app, status, warning):
        return super().get_output(app, status, warning)

    @with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='text')
    def get_expected(self, app, status, warning):
        return super().get_expected(app, status, warning)

# Test using Sphinx html builder
class ExtensionHtmlTestcase(ExtensionTestcase):
    @with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='html')
    def get_output(self, app, status, warning):
        return super().get_output(app, status, warning)

    @with_app(confdir=testenv.testdir, create_new_srcdir=True, buildername='html')
    def get_expected(self, app, status, warning):
        return super().get_expected(app, status, warning)

def _get_text_testcases(path):
    for f in testenv.get_testcase_filenames(path):
        yield ExtensionTextTestcase(f)

def _get_html_testcases(path):
    for f in testenv.get_testcase_filenames(path):
        yield ExtensionHtmlTestcase(f)

@pytest.mark.parametrize('testcase', _get_text_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_directive_text(testcase):
    testcase.run_test()

@pytest.mark.full
@pytest.mark.parametrize('testcase', _get_html_testcases(testenv.testdir),
                         ids=testenv.get_testid)
def test_directive_html(testcase):
    testcase.run_test()
