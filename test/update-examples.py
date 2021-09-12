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
    options = testenv.get_testcase_options(testcase)

    directive = options.get('directive')
    if directive:
        namespace_push = f'.. c:namespace-push:: {title}'
        namespace_pop = '.. c:namespace-pop::'
    else:
        directive = 'autodoc'
        namespace_push = ''
        namespace_pop = ''
    arguments = options.get('directive-arguments', '')
    sep = ' ' if arguments else ''

    options = options.get('directive-options', {})

    directive_options_str = ''
    for key, value in options.items():
        if isinstance(value, list):
            value = ', '.join(value)
        directive_options_str += f':{key}: {value}\n'
    directive_options_str = directive_options_str.strip()

    print(f'''{title}
{get_title_underline(title)}

Source
~~~~~~

.. literalinclude:: {input_filename}
   :language: C

Directive
~~~~~~~~~

.. code-block:: rest

   .. c:{directive}:: {input_filename}{sep}{arguments}
{indent(directive_options_str, '      ')}

Output
~~~~~~

{namespace_push}

.. c:{directive}:: {input_filename}{sep}{arguments}
{indent(directive_options_str, '   ')}

{namespace_pop}

''')

if __name__ == '__main__':
    print_header()
    for f in testenv.get_testcases(testenv.testdir):
        if os.path.basename(f).startswith('example-'):
            print_example(f)
