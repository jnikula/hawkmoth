# Copyright (c) 2021 Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Compiler helpers
================

This module provides helper functions to access compiler information outside of
the Clang Python Bindings, for example system include paths.
"""

import subprocess
from sphinx.util import logging

logger = logging.getLogger(__name__)

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

def _get_include_paths(cpath, lang):
    try:
        result = subprocess.run([cpath, '-x', lang, '-E', '-Wp,-v', '-'],
                                stdin=subprocess.DEVNULL,
                                capture_output=True,
                                check=True,
                                text=True)
    except FileNotFoundError:
        logger.warning(f"get_include_args: {lang} compiler not found ('{cpath}')")
        return []

    except subprocess.CalledProcessError:
        logger.warning(f"get_include_args: incompatible {lang} compiler ('{cpath}')")
        return []

    if result.returncode != 0:
        logger.warning(f"get_include_args: incompatible {lang} compiler ('{cpath}')")
        return []

    return _get_paths_from_output(result.stderr)

def get_include_args(cpath='clang', lang='c', cc_path=None):
    if cc_path is not None:
        cpath = cc_path
        logger.warning('get_include_args: `cc_path` argument has been deprecated; use `cpath` instead')  # noqa: E501

    return ['-nostdinc'] + [f'-I{path}' for path in _get_include_paths(cpath, lang)]

if __name__ == '__main__':
    import pprint
    import sys

    compiler = sys.argv[1] if len(sys.argv) > 1 else 'clang'

    pprint.pprint(get_include_args(compiler))
