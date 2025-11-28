#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2021 Jani Nikula <jani@nikula.org>
# SPDX-License-Identifier: BSD-2-Clause

import os
import re
import sys

from test import testenv


class ExampleTestcase(testenv.Testcase):
    pass


def get_title(testcase):
    return testcase.options.get("example-title")


def get_title_underline(title):
    return "-" * len(title)


def indent(s, prefix=""):
    lines = [f"{prefix}{line}".rstrip() for line in s.splitlines()]

    return "\n".join(lines)


# Even though we're generating the file, we're generating it from sources that
# have copyright and license, so replicate that here too.
def print_header():
    print("""
.. SPDX-FileCopyrightText: 2017 Jani Nikula <jani@nikula.org>
.. SPDX-FileCopyrightText: 2019 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
.. SPDX-License-Identifier: BSD-2-Clause

.. Generated using update-examples, do not edit manually!

.. _examples:

Examples
========

This page showcases Hawkmoth in action.

The ``[source]`` links are optional, and can be enabled via the
:py:data:`hawkmoth_source_uri` option.

.. contents::
   :local:
   :depth: 1

""")


def print_title(testcases):
    titles = {get_title(testcase) for testcase in testcases if get_title(testcase)}
    title = ", ".join(sorted(titles))

    print(f"""{title}
{get_title_underline(title)}
""")


def print_source(testcases, input_filename):
    domain = {testcase.directives[0].domain for testcase in testcases}
    if len(domain) == 1:
        language = "C" if next(iter(domain)) == "c" else "C++"
    else:
        print(f"WARNING: {input_filename} used in multiple domains", file=sys.stderr)
        language = "C++"

    literal_include = f"../test/examples/{input_filename}"

    print(f"""Source
~~~~~~

.. literalinclude:: {literal_include}
   :language: {language}
   :caption: {input_filename}
""")


def print_example(testcase):
    options = testcase.options
    domain = testcase.directives[0].domain

    if options.get("example-use-namespace"):
        # Generate namespace from relative path to YAML without extension
        relative = os.path.relpath(testcase.filename, start=testenv.testdir)
        relative, _ = os.path.splitext(relative)

        namespace = "namespace_" + re.sub(r"[^a-zA-Z0-9]", "_", relative)

        namespace_push = f".. {domain}:namespace-push:: {namespace}\n\n"
        namespace_pop = f"\n.. {domain}:namespace-pop::\n"
    else:
        namespace_push = ""
        namespace_pop = ""

    directive_str = testcase.directives[0].get_directive_string()

    print(f"""Directive
~~~~~~~~~

.. code-block:: rest

{indent(directive_str, "   ")}

Output
~~~~~~

{namespace_push}{directive_str}{namespace_pop}
""")


def testcase_key(testcase):
    return int(testcase.options.get("example-priority", 0))


def examples_key(item):
    (_, testcases) = item

    return min([testcase_key(testcase) for testcase in testcases])


def get_examples():
    examples = {}

    for f in testenv.get_testcase_filenames(os.path.join(testenv.testdir, "examples")):
        testcase = ExampleTestcase(f)

        if len(testcase.directives) != 1:
            print(f"WARNING: {f} uses multiple directives", file=sys.stderr)

        input_filename = os.path.basename(testcase.directives[0].get_input_filename())

        if input_filename in examples:
            examples[input_filename].append(testcase)
        else:
            examples[input_filename] = [testcase]

    return examples


if __name__ == "__main__":
    print_header()

    for source, testcases in sorted(get_examples().items(), key=examples_key):
        print_title(testcases)
        print_source(testcases, source)
        for testcase in sorted(testcases, key=testcase_key):
            print_example(testcase)
