#!/usr/bin/env python2.7

from setuptools import setup

description = '''Adds a command to dynamically get the version from the VCS of choice'''

with open('README.txt', 'r') as f:
    long_description = f.read()

setup(
    author='Joost Molenaar',
    author_email='j.j.molenaar@gmail.com',
    url='https://github.com/j0057/setuptools-version-command',
    name='setuptools-version-command',
    version='1.0',
    description=description,
    long_description=long_description,
    packages=['setuptools_version_command'],
    entry_points={
        'distutils.setup_keywords': [
            'version_command = setuptools_version_command:execute_version_command'
        ]
    })
