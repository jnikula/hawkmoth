# SPDX-FileCopyrightText: 2017 Jani Nikula <jani@nikula.org>
# SPDX-FileCopyrightText: 2018 Bruno Santos <brunomanuelsantos@tecnico.ulisboa.pt>
# SPDX-License-Identifier: BSD-2-Clause
#
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Use the installed Hawkmoth package for CI, testing, and Read the Docs, while
# allowing documentation build using Hawkmoth from the source tree.
if not tags.has("use-installed-hawkmoth") and "READTHEDOCS" not in os.environ:
    sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Hawkmoth"
copyright = "2017-2023, Jani Nikula and contributors"
author = "Jani Nikula"

with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), "../src/hawkmoth/VERSION")
) as version_file:
    version = version_file.read().strip()
    release = version

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "hawkmoth",
    "hawkmoth.ext.javadoc",
    "hawkmoth.ext.napoleon",
    "sphinx.ext.intersphinx",
]

# If your documentation needs a minimal Sphinx version, state it here.
#
# The documentation uses the intersphinx explicit external reference role. Note
# that this is not the same as Hawkmoth extension minimum version requirement.
needs_sphinx = "4.4"

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "examples"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None

# -- Options for Hawkmoth ----------------------------------------------------
# https://jnikula.github.io/hawkmoth/dev/extension.html#configuration

# Setup Clang on Read The Docs
if "READTHEDOCS" in os.environ:
    from hawkmoth.util import readthedocs

    readthedocs.clang_setup()

hawkmoth_root = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../test/examples")

source_uri = "https://github.com/jnikula/hawkmoth/tree/{version}/test/examples/{{source}}#L{{line}}"
source_version = f"v{version}" if len(version.split(".")) == 3 else "master"

hawkmoth_source_uri = source_uri.format(version=source_version)

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    "description": "Sphinx Autodoc for C",
    "extra_nav_links": {
        "GitHub": "https://github.com/jnikula/hawkmoth",
        "PyPI": "https://pypi.org/project/hawkmoth",
    },
    "sidebar_width": "280px",
    "page_width": "1000px",
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
html_sidebars = {
    "**": [
        "about.html",
        "versions.html",
        "navigation.html",
        "relations.html",
        "searchbox.html",
        "donate.html",
    ]
}

# -- Cross project references ------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master", None),
}


def setup(app):
    app.add_object_type("confval", "confval")
    app.add_object_type("event", "event", "pair: %s; event")
