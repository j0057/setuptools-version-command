#!/usr/bin/env python2.7

import os
import setuptools
import setuptools.command.test

if not 'SETUPTOOLS_ALLOW_DOWNLOAD' in os.environ:
    os.environ['HTTP_PROXY']  = '127.0.0.1:65534'
    os.environ['HTTPS_PROXY'] = '127.0.0.1:65535'

class PyTest(setuptools.command.test.test):
    def initialize_options(self):
        setuptools.command.test.test.initialize_options(self)

    def finalize_options(self):
        setuptools.command.test.test.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # XXX: If I import pytest and call pytest.main, the setuptools_version_command module is already loaded, I think because
        # setuptools has it loaded as an entry_point. That means the top-level statements don't get executed while coverage is
        # watching, which means 16 missed statements. Reloading the module doesn't work, so the next best thing is to just run
        # the tests in a new process. However, it does mean that py.test has to be installed in either the system or the user's
        # site-packages.

        # import pytest
        # pytest.main()

        os.system('py.test')

with open('README.rst', 'r') as f:
    long_description = f.read()

setuptools.setup(**{
    'name': 'setuptools-version-command',
    'description':  'Adds a command to dynamically get the version from the VCS of choice',
    'long_description': long_description,
    'license': 'http://opensource.org/licenses/MIT',

    'url': 'https://github.com/j0057/setuptools-version-command',
    'author': 'Joost Molenaar',
    'author_email': 'j.j.molenaar@gmail.com',

    'version': '2.1a0',

    'classifiers': [
        'Framework :: Setuptools Plugin',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: 2.7'
    ],

    'py_modules': ['setuptools_version_command'],

    'install_requires': ['setuptools'],
    'tests_require': [
        'pytest',
        'pytest-cov',
        'pytest-flakes'
    ],

    'entry_points': {
        'distutils.setup_keywords': [
            'version_command = setuptools_version_command:validate_version_command_keyword'
        ],
        'egg_info.writers': [
            'version.txt      = setuptools_version_command:write_metadata_value',
            'version_full.txt = setuptools_version_command:write_metadata_value'
        ]
    }
})
