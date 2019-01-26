# Copyright (c) 2018, Jani Nikula <jani@nikula.org>
# Licensed under the terms of BSD 2-Clause, see LICENSE for details.

import setuptools

with open('README.rst', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name = 'hawkmoth',
    version = '0.2',
    author = 'Jani Nikula',
    author_email = 'jani@nikula.org',
    license = '2-Clause BSD',
    description = 'Hawkmoth - Sphinx Autodoc for C',
    long_description = long_description,
    long_description_content_type = 'text/x-rst',
    url = 'https://github.com/jnikula/hawkmoth',
    packages = [
        'hawkmoth',
    ],
    install_requires = [
        'sphinx',
        # 'clang', # depend on distro packaging
    ],
    extras_requires = {
        'dev': [
            'sphinx-testing'
        ],
    },
    python_requires = '~=3.4',
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Sphinx :: Extension',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Documentation :: Sphinx',
        'Topic :: Software Development :: Documentation',
    ],
    keywords = 'python sphinx autodoc documentation c',
    project_urls = {
        'Documentation': 'https://hawkmoth.readthedocs.io/en/latest/',
        'Mailing List': 'https://www.freelists.org/list/hawkmoth',
    }
)
