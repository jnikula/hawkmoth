# Copyright (c) 2021, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import pytest

# Enable introspection on assertions in testenv
pytest.register_assert_rewrite('test.testenv')
