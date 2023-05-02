#!/usr/bin/env python3
# Copyright (c) 2018-2023, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import shutil
import tempfile

import pytest
from sphinx.application import Sphinx

from test import testenv

class ExtensionTestcase(testenv.Testcase):
    def __init__(self, filename, buildername):
        super().__init__(filename)
        self._buildername = buildername

    def _get_suffix(self):
        return 'txt' if self._buildername == 'text' else self._buildername

    def _sphinx_build(self, srcdir):
        outdir = os.path.join(srcdir, self._buildername)
        doctreedir = os.path.join(srcdir, 'doctrees')

        app = Sphinx(srcdir=srcdir, confdir=testenv.testdir, outdir=outdir,
                     doctreedir=doctreedir, buildername=self._buildername)

        # Set root to the directory the testcase yaml is in, because the
        # filenames in yaml are relative to it.
        app.config.hawkmoth_root = os.path.dirname(self.filename)

        # Hack: It's not possible to disable search via configuration
        app.builder.search = False

        app.build()

        output_suffix = self._get_suffix()
        output_filename = os.path.join(app.outdir, f'index.{output_suffix}')

        return testenv.read_file(output_filename), None

    def _sphinx_build_str(self, input_str):
        with tempfile.TemporaryDirectory() as srcdir:
            with open(os.path.join(srcdir, 'index.rst'), 'w') as f:
                f.write(input_str)
            return self._sphinx_build(srcdir)

    def _sphinx_build_file(self, input_filename):
        with tempfile.TemporaryDirectory() as srcdir:
            shutil.copyfile(input_filename, os.path.join(srcdir, 'index.rst'))
            return self._sphinx_build(srcdir)

    def get_output(self):
        return self._sphinx_build_str(self.get_directive_string())

    def get_expected(self):
        return self._sphinx_build_file(self.get_expected_filename())

def _get_extension_testcases(path, buildername):
    for f in testenv.get_testcase_filenames(path):
        yield ExtensionTestcase(f, buildername)

# Test using Sphinx plain text builder
@pytest.mark.parametrize('testcase', _get_extension_testcases(testenv.testdir, 'text'),
                         ids=testenv.get_testid)
def test_directive_text(testcase):
    testcase.run_test()

# Test using Sphinx html builder
@pytest.mark.full
@pytest.mark.parametrize('testcase', _get_extension_testcases(testenv.testdir, 'html'),
                         ids=testenv.get_testid)
def test_directive_html(testcase):
    testcase.run_test()
