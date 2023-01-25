#!/usr/bin/env python3
# Copyright (c) 2021, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import os
import re

import testenv

class ExampleTestcase(testenv.Testcase):
    pass

def get_title(testcase):
    return testcase.options.get('example-title')

def get_title_underline(title):
    return '-' * len(title)

def indent(s, prefix=''):
    lines = [f'{prefix}{line}'.rstrip() for line in s.splitlines()]

    return '\n'.join(lines)

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

def print_title(testcases):
    titles = set(get_title(testcase) for testcase in testcases if get_title(testcase))
    title = ', '.join(sorted(titles))

    print(f'''{title}
{get_title_underline(title)}
''')

def print_source(input_filename):
    literal_include = f'../test/examples/{input_filename}'

    print(f'''Source
~~~~~~

.. literalinclude:: {literal_include}
   :language: C
   :caption: {input_filename}
''')

def print_example(testcase):
    options = testcase.options
    domain = options.get('domain')

    if options.get('example-use-namespace'):
        # Generate namespace from relative path to YAML without extension
        relative = os.path.relpath(testcase.filename, start=testenv.testdir)
        relative, _ = os.path.splitext(relative)

        namespace = 'namespace_' + re.sub(r'[^a-zA-Z0-9]', '_', relative)

        namespace_push = f'.. {domain}:namespace-push:: {namespace}\n\n'
        namespace_pop = f'\n.. {domain}:namespace-pop::\n'
    else:
        namespace_push = ''
        namespace_pop = ''

    directive_str = testcase.get_directive_string()

    print(f'''Directive
~~~~~~~~~

.. code-block:: rest

{indent(directive_str, '   ')}

Output
~~~~~~

{namespace_push}{directive_str}{namespace_pop}
''')

def testcase_key(testcase):
    return int(testcase.options.get('example-priority', 0))

def examples_key(item):
    (_, testcases) = item

    return min([testcase_key(testcase) for testcase in testcases])

def _get_example_testcases(path):
    for f in testenv.get_testcase_filenames(path):
        if os.path.basename(f).startswith('example-'):
            yield ExampleTestcase(f)

def get_examples():
    examples = {}

    for testcase in _get_example_testcases(os.path.join(testenv.testdir, 'examples')):
        input_filename = os.path.basename(testcase.get_input_filename())

        if input_filename in examples:
            examples[input_filename].append(testcase)
        else:
            examples[input_filename] = [testcase]

    return examples

if __name__ == '__main__':
    print_header()

    for source, testcases in sorted(get_examples().items(), key=examples_key):
        print_title(testcases)
        print_source(source)
        for testcase in sorted(testcases, key=testcase_key):
            print_example(testcase)
