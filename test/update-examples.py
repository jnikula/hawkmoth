#!/usr/bin/env python3
# Copyright (c) 2021, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import re

import testenv

def get_title(testcase):
    basename = os.path.basename(testcase)

    title = re.sub(r'^example-[0-9]+-([a-zA-Z0-9_-]+).yaml$', r'\1', basename)
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
    options = testenv.get_testcase_options(testcase)
    input_filename = testenv.get_input_filename(options)
    literal_include = f'../test/{input_filename}'

    directive = options.get('directive')
    if directive:
        namespace_push = f'.. c:namespace-push:: {title}\n\n'
        namespace_pop = '\n.. c:namespace-pop::\n'
    else:
        namespace_push = ''
        namespace_pop = ''

    directive_str = testenv.get_directive_string(options)

    print(f'''{title}
{get_title_underline(title)}

Source
~~~~~~

.. literalinclude:: {literal_include}
   :language: C
   :caption: {input_filename}

Directive
~~~~~~~~~

.. code-block:: rest

{indent(directive_str, '   ')}

Output
~~~~~~

{namespace_push}{directive_str}{namespace_pop}
''')

if __name__ == '__main__':
    print_header()
    for testcase in testenv.get_testcases(testenv.testdir):
        if os.path.basename(testcase).startswith('example-'):
            print_example(testcase)
