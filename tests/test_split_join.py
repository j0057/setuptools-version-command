from __future__ import unicode_literals

import sys

import pytest

from setuptools_version_command import _split_version, _join_version

def test_regex_roundtrip():
    v1 = 'v1!2.3a4.post5.dev6'
    vd = _split_version(v1)
    v2 = _join_version(vd)
    assert v1 == v2

def test_regex_error():
    with pytest.raises(Exception) as e:
        _split_version('1.2.foo3')
    assert e.value.args[0] == ('Can\'t parse version \'1.2.foo3\' as PEP440 version'
                               if sys.version_info[0] == 3 else
                               'Can\'t parse version u\'1.2.foo3\' as PEP440 version')
