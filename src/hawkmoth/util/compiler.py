# Copyright (c) 2021 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Compiler helpers
================

This module provides helper functions to access compiler information outside of
the Clang Python Bindings, for example system include paths.
"""

import subprocess

def _removesuffix(s, suffix):
    if suffix and s.endswith(suffix):
        return s[:-len(suffix)]
    else:
        return s[:]

def _get_paths_from_output(output):
    started = False
    for line in output.splitlines():
        if not started:
            if line == '#include <...> search starts here:':
                started = True
            continue

        if line == 'End of search list.':
            break

        # Clang on macOS may print this.
        line = _removesuffix(line, '(framework directory)')

        yield line.strip()

def _get_include_paths(cc_path):
    result = subprocess.run([cc_path, '-E', '-Wp,-v', '-'],
                            stdin=subprocess.DEVNULL,
                            capture_output=True,
                            check=True,
                            text=True)

    return _get_paths_from_output(result.stderr)

def get_include_args(cc_path='clang'):
    return [f'-I{path}' for path in _get_include_paths(cc_path)]

if __name__ == '__main__':
    import pprint
    import sys

    cc_path = sys.argv[1] if len(sys.argv) > 1 else 'clang'

    pprint.pprint(get_include_args(cc_path))
