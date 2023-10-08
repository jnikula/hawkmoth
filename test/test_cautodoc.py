#!/usr/bin/env python3
# Copyright (c) 2018-2023, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import io
import os
import re
import shutil
import tempfile

import pytest
from sphinx.application import Sphinx
from sphinx.util.docutils import docutils_namespace, patch_docutils
from sphinx.util import console

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
        confdir = testenv.testdir

        # Don't emit color codes in Sphinx status/warning output
        console.nocolor()

        warning = io.StringIO()

        with patch_docutils(confdir), docutils_namespace():
            app = Sphinx(srcdir=srcdir, confdir=confdir, outdir=outdir,
                         doctreedir=doctreedir, buildername=self._buildername,
                         warning=warning)

            # Ensure there are no errors with app creation.
            assert warning.getvalue() == ''

            # Set root to the directory the testcase yaml is in, because the
            # filenames in yaml are relative to it.
            app.config.hawkmoth_root = os.path.dirname(self.filename)

            # Hack: It's not possible to disable search via configuration
            app.builder.search = False

            app.build()

            output_suffix = self._get_suffix()
            output_filename = os.path.join(app.outdir, f'index.{output_suffix}')

        # Remove paths from warning output for comparison
        output_errors = re.sub(rf'(?m)^{srcdir}/index.rst:[0-9]+: ([^:]*: )(/[a-zA-Z0-9._-]+)*/',
                               '\\1', warning.getvalue())

        return testenv.read_file(output_filename), output_errors

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
        input_str = ''.join([d.get_directive_string() for d in self.directives])

        return self._sphinx_build_str(input_str)

    def get_expected(self):
        expected_docs, _ = self._sphinx_build_file(self.get_expected_filename())
        expected_errors = testenv.read_file(self.get_stderr_filename(), optional=True)

        return expected_docs, expected_errors

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
