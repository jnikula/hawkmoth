#!/usr/bin/env python3
# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import unittest

import testenv
from hawkmoth.parser import parse

def _get_output(input_filename, **options):
    docs_str = ''
    errors_str = ''

    docs, errors = parse(input_filename, **options)

    for (doc, meta) in docs:
        docs_str += doc + '\n'

    for (severity, filename, lineno, msg) in errors:
        errors_str += '{}: {}: {}\n'.format(severity.name, lineno, msg)

    return docs_str, errors_str

def _get_expected(input_filename, **options):
    return testenv.read_file(input_filename, ext='rst'), \
        testenv.read_file(input_filename, ext='stderr')

class ParserTest(unittest.TestCase):
    pass

testenv.assign_test_methods(ParserTest, _get_output, _get_expected)

if __name__ == '__main__':
    unittest.main()
