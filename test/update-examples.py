#!/usr/bin/env python3
# Copyright (c) 2021, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import re

import testenv

def get_title(testcase):
    basename = os.path.basename(testcase)

    title = re.sub(r'^example-[0-9]+-([a-zA-Z0-9_-]+).c$', r'\1', basename)
    title = title.replace('-', ' ')
    title = title.capitalize()

    return title

def get_title_underline(title):
    return '-' * len(title)

def indent(s, prefix=''):
    return re.sub(r'(?m)^', prefix, s)

def print_header():
    print('''
.. Generated using update-examples, do not edit manually!

.. _examples:

Examples
========

This page showcases Hawkmoth in action.

.. contents::
   :local:
   :depth: 1

.. only:: not have_hawkmoth

   .. note:: The documentation you are viewing was built without Hawkmoth and/or
             its dependencies (perhaps on https://readthedocs.org/). The output
             seen below was pre-generated statically using Hawkmoth, and should
             closely reflect actual results.
''')

def print_example(testcase):
    title = get_title(testcase)
    basename = os.path.basename(testcase)
    input_filename = f'examples/{basename}'
    options_dict = testenv.get_testcase_options(testcase)
    options = ''
    for key, value in options_dict.items():
        options += f':{key}: {value}\n'
    options = options.strip()

    print(f'''{title}
{get_title_underline(title)}

Source
~~~~~~

.. literalinclude:: {input_filename}
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:autodoc:: {input_filename}
{indent(options, '      ')}

Output
~~~~~~

.. c:autodoc:: {input_filename}
{indent(options, '   ')}
''')

if __name__ == '__main__':
    print_header()
    for f in testenv.get_testcases(testenv.testdir):
        if os.path.basename(f).startswith('example-'):
            print_example(f)
