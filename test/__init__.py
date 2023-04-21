# Copyright (c) 2021, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import pytest
import os
import sys

# Use 'our' version of the module.
sys.path.insert(0, os.path.abspath('src'))

# Enable introspection on assertions in testenv
pytest.register_assert_rewrite('test.testenv')
