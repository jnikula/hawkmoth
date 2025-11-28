# SPDX-FileCopyrightText: 2021 Jani Nikula <jani@nikula.org>
# SPDX-License-Identifier: BSD-2-Clause

import pytest

# Enable introspection on assertions in testenv
pytest.register_assert_rewrite("test.testenv")
