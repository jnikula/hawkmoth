#!/usr/bin/env python3
# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import shutil
import unittest

import testenv
from sphinx_testing import with_app

class DirectiveTest(unittest.TestCase):

    def _setup_src(self, srcdir, testcase_in):
        testcase_out = testenv.modify_filename(testcase_in, dir=srcdir)

        # use the pre-generated rst as comparison data
        shutil.copyfile(testenv.modify_filename(testcase_in, ext='stdout'),
                        testenv.modify_filename(testcase_out, ext='expected.rst'))

        # set up an rst file to run the extension
        shutil.copyfile(testcase_in, testcase_out)
        options = testenv.get_testcase_options(testcase_in)

        with open(testenv.modify_filename(testcase_out, ext='output.rst'), 'w') as file:
            fmt = '.. c:autodoc:: {source}\n'
            file.write(fmt.format(source=os.path.basename(testcase_out)))
            for key in options.keys():
                fmt = '   :{key}: {value}\n'
                file.write(fmt.format(key=key, value=options[key]))

    def _check_out(self, outdir, testcase_in):
        testcase_out = testenv.modify_filename(testcase_in, dir=outdir)

        # compare output from the pre-generated rst against the output generated
        # by the extension

        output = testenv.read_file(testenv.modify_filename(testcase_out,
                                                           ext='output.txt'))

        expected = testenv.read_file(testenv.modify_filename(testcase_out,
                                                             ext='expected.txt'))

        self.assertEqual(expected, output)

    # Use copy_srcdir_to_tmpdir=False and outdir='some-dir' for debugging
    @with_app(srcdir=os.path.join(testenv.testdir, 'sphinx'),
              buildername='text', copy_srcdir_to_tmpdir=True)
    def test_directive(self, app, status, warning):
        testcases = list(testenv.get_testcases(testenv.testdir))

        for f in testcases:
            self._setup_src(app.srcdir, f)

        app.build()

        for f in testcases:
            with self.subTest(source=os.path.basename(f)):
                self._check_out(app.outdir, os.path.basename(f))

if __name__ == '__main__':
    unittest.main()
