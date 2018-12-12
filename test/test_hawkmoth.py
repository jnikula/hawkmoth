#!/usr/bin/env python3
# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import unittest

import testenv
from hawkmoth import hawkmoth

class ParserTest(unittest.TestCase):
    def _run_test(self, input_filename):
        # sanity check
        self.assertTrue(os.path.isfile(input_filename))

        options = testenv.get_testcase_options(input_filename)
        output = hawkmoth.parse_to_string(input_filename, False, **options)
        expected = testenv.read_file(input_filename, ext='stdout')

        self.assertEqual(expected, output)

    def _run_dir(self, path):
        # sanity check
        self.assertTrue(os.path.isdir(path))

        with self.subTest(path=path):
            for f in testenv.get_testcases(path):
                with self.subTest(source=os.path.basename(f)):
                    self._run_test(f)

    def test_parser(self):
        self._run_dir(testenv.testdir)

if __name__ == '__main__':
    unittest.main()
