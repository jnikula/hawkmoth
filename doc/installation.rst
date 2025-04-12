.. SPDX-FileCopyrightText: 2020 Jani Nikula <jani@nikula.org>
.. SPDX-License-Identifier: BSD-2-Clause

.. _installation:

Installation
============

You can install the Hawkmoth Python package and most of its dependencies from
PyPI_ with:

.. code-block:: shell

  pip install hawkmoth

However, you'll also need to install Clang and Clang Python Bindings through
your distro's package manager; they are not available via PyPI. This is
typically the biggest hurdle in getting your Hawkmoth setup to work.

.. _PyPI: https://pypi.org/project/hawkmoth/

Clang Distro Install
--------------------

This step is necessarily distro specific.

For example, in recent Debian and Ubuntu:

.. code-block:: shell

   apt install python3-clang

Clang Python Bindings
---------------------

There are **unofficial** Clang Python Bindings available in PyPI. They may be
helpful in some scenarios, but they will not include the binary ``libclang``,
and the provided Python Bindings might not be compatible with the library
provided in your system. It's recommended to use the bindings from the distro,
but if you need to install the ``clang`` package from PyPI, it's recommended to
use the same major varsion for both system ``libclang`` and Python ``clang``.

If the Clang Python Bindings are unable to find ``libclang``, for whatever
reason, there are some tricks to try:

* Set the library path in shell:

  .. code-block:: shell

     export LD_LIBRARY_PATH=$(llvm-config --libdir)

* Set the library path in ``conf.py``:

  .. code-block:: python

     from clang.cindex import Config
     Config.set_library_path('/path/to/clang')

* Set the library name in ``conf.py``, possibly combined with
  ``LD_LIBRARY_PATH``:

  .. code-block:: python

     from clang.cindex import Config
     Config.set_library_file('libclang.so')

* Set the library name with full path in ``conf.py``:

  .. code-block:: python

     from clang.cindex import Config
     Config.set_library_file('/path/to/clang/libclang.so')

Virtual Environment
-------------------

If you're installing Hawkmoth in a Python virtual environment, use the
``--system-site-packages`` option when creating the virtual environment to make
the distro Clang package available to the virtual environment. For example:

.. code-block:: shell

   python3 -m venv --system-site-packages .venv

Read the Docs
-------------

It's possible to set up Hawkmoth based documentation on `Read the Docs`_
(RTD). Use the ``.readthedocs.yaml`` `configuration file`_ to install system
``libclang`` and specify a Python ``requirements.txt`` file:

.. code-block:: yaml

   build:
     os: ubuntu-22.04
     tools:
       python: "3.11"
     apt_packages:
       - libclang-14-dev

   python:
     install:
       - requirements: requirements.txt

In the ``requirements.txt`` file, specify the dependencies::

  clang==14.0.6
  hawkmoth==0.14.0

To ensure the system ``libclang`` and Python ``clang`` compatibility, it's
recommended to specify matching major versions. RTD also recommends pinning all
the versions to avoid unexpected build errors.

If the Clang Python Bindings fail to find ``libclang`` automatically, try adding
this snippet to your ``conf.py``:

.. code-block:: python

   from hawkmoth.util import readthedocs

   readthedocs.clang_setup()

This will try to find ``libclang`` on RTD, and configure Clang Python Bindings
to use it.

.. _configuration file: https://docs.readthedocs.io/en/stable/config-file/v2.html

.. _Read the Docs: https://readthedocs.org/

.. _dependency documentation: https://docs.readthedocs.io/en/stable/guides/specifying-dependencies.html
