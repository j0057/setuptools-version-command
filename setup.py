#!/usr/bin/env python2.7

from setuptools import setup

description = '''Adds a command to dynamically get the version from the VCS of choice'''

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
    name='setuptools-version-command',
    author='Joost Molenaar',
    author_email='j.j.molenaar@gmail.com',
    url='https://github.com/j0057/setuptools-version-command',
    version='1.3.4',
    description=description,
    long_description=long_description,
    py_modules=['setuptools_version_command'],
    entry_points={
        'distutils.setup_keywords': [
            'version_command = setuptools_version_command:validate_version_command_keyword'
        ],
        'egg_info.writers': [
            'version.txt      = setuptools_version_command:write_metadata_value',
            'version_full.txt = setuptools_version_command:write_metadata_value'
        ]
    })
