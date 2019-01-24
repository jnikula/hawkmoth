#!/usr/bin/env python3
# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import unittest

import testenv
from hawkmoth import hawkmoth

def _get_output(input_filename, **options):
    return hawkmoth.parse_to_string(input_filename, False, **options)

def _get_expected(input_filename, **options):
    return testenv.read_file(input_filename, ext='stdout')

class ParserTest(unittest.TestCase):
    pass

testenv.assign_test_methods(ParserTest, _get_output, _get_expected)

if __name__ == '__main__':
    unittest.main()
