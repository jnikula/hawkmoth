.. _installation:

Installation
============

You can install the Hawkmoth Python package and most of its dependencies from
PyPI_ with:

.. code-block:: shell

  pip install hawkmoth

However, you'll also need to install Clang and Clang Python Bindings through
your distro's package manager; they are not available via PyPI_. This is
typically the biggest hurdle in getting your Hawkmoth setup to work.

.. _PyPI: https://pypi.org/project/hawkmoth/

Clang Distro Install
--------------------

This step is necessarily distro specific.

For example, in Debian Bullseye:

.. code-block:: shell

   apt install python3-clang

Clang Python Bindings
---------------------

There are **unofficial** Clang Python Bindings available in PyPI_. They may be
helpful in some scenarios (for example Debian Buster not packaging Clang Python
Bindings for Python 3 at all), but they will not include the binary
``libclang``, and the provided Python Bindings might not be compatible with the
library provided in your system.

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

Docker
------

It's also possible to set up a Docker container to run Sphinx with
Hawkmoth. There are no official images for this at this time, but please have a
look at the ``Dockerfile`` in the `Hawkmoth source repository`_ for a starting
point; the file is used for testing during Hawkmoth development.

.. _Hawkmoth source repository: https://github.com/jnikula/hawkmoth

Read the Docs
-------------

It's possible to set up Hawkmoth based documentation on `Read the Docs`_ (RTD),
and Hawkmoth provides a helper for configuration. There's a caveat, though: This
is not based on the official RTD documentation, and might cease to work at any
time.

First, add a ``requirements.txt`` file to your project according to RTD
`dependency documentation`_ to have RTD install some required dependencies::

  clang>=6
  hawkmoth>=0.7

Next, add this snippet to your ``conf.py``:

.. code-block:: python

   from hawkmoth.util import readthedocs

   readthedocs.clang_setup()

This will try to find ``libclang`` on RTD, and configure Clang Python Bindings
to use it.

.. _Read the Docs: https://readthedocs.org/

.. _dependency documentation: https://docs.readthedocs.io/en/stable/guides/specifying-dependencies.html
