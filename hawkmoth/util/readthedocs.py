# Copyright (c) 2021, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.
"""
Read the Docs Helpers
=====================

Helpers for setting up and using Hawkmoth on Read the Docs.
"""

import os
import subprocess

def clang_setup(force=False):
    """Try to find and configure libclang location on RTD."""
    if 'READTHEDOCS' in os.environ or force:
        try:
            result = subprocess.run(['llvm-config', '--libdir'],
                                    check=True, capture_output=True, encoding='utf-8')
            libdir = result.stdout.strip()

            # For some reason there is no plain libclang.so symlink on RTD.
            from clang.cindex import Config
            Config.set_library_file(os.path.join(libdir, 'libclang.so.1'))
        except Exception as e:
            print(e)
