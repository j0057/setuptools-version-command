from __future__ import unicode_literals

import subprocess
import sys

try:
    import __builtin__
except ImportError:
    import builtins as __builtin__

import pytest

from setuptools_version_command import _get_scm_version, _read_version, \
                                       validate_version_command_keyword, write_metadata_value

class fake_obj(object):
    def __init__(self, props={}):
        for (k,v) in props.items():
            setattr(self, k, fake_obj(v) if isinstance(v, dict) else v)

class fake_func(object):
    def __init__(self):
        self.result = None
        self.exc = None
        self.calls = []
    def __call__(self, *a, **k):
        self.calls.append((a, k))
        if self.exc: raise self.exc
        return self.result

@pytest.fixture
def git_describe(monkeypatch):
    monkeypatch.setattr(subprocess, 'check_output', fake_func())
    return subprocess.check_output

@pytest.fixture
def fake_file(monkeypatch):
    class open_(dict):
        content = {}
        def __init__(self, fn, mode):
            self.fn = fn
        def __enter__(self, *_, **__):
            return self
        def __exit__(self, *_, **__):
            pass
        def read(self):
            return self.content[self.fn]
    monkeypatch.setattr(__builtin__, 'open', open_)
    return open_
 
def test_get_scm_version(git_describe):
    git_describe.result = b'1.2-0-abcd123\n'
    result = _get_scm_version('git describe', 'pep440-git', {})
    assert result == ('1.2', '1.2-0-abcd123')

def test_read_version(fake_file):
    fake_file.content['a'] = 'hi'
    result = _read_version('a')
    assert result == 'hi'

def test_keyword(git_describe, fake_file):
    git_describe.result = b'1.2-0-abcd123\n'
    dist = fake_obj({ 'metadata': { 'name': 'spam' } })

    validate_version_command_keyword(dist, 'version_command', ('git describe', 'pep440-git', '-'))

    assert dist.metadata.version == '1.2'
    assert dist.metadata.version_full == '1.2-0-abcd123'

def test_keyword_cached(git_describe, fake_file):
    git_describe.exc = Exception('error')
    fake_file.content['spam.egg-info/version.txt'] = '1.2'
    fake_file.content['spam.egg-info/version_full.txt'] = '1.2-0-abcd123'
    dist = fake_obj({ 'metadata': { 'name': 'spam' } })

    validate_version_command_keyword(dist, 'version_command', ('git describe', 'pep440-git', '-'))

    assert dist.metadata.version == '1.2'
    assert dist.metadata.version_full == '1.2-0-abcd123'

def test_keyword_not_git_repo(git_describe, fake_file):
    git_describe.exc = Exception('error')
    dist = fake_obj({ 'metadata': { 'name': 'spam' } })

    with pytest.raises(Exception) as e:
        validate_version_command_keyword(dist, 'version_command', ('git describe', 'pep440-git', '-'))

    assert e.value.args[0].startswith('Could not find version')

def test_keyword_closed_tag(git_describe, fake_file):
    git_describe.result = b'1.2.dev5-3-abcd123\n'
    dist = fake_obj({ 'metadata': { 'name': 'spam' } })

    with pytest.raises(Exception) as e:
        validate_version_command_keyword(dist, 'version_command', ('git describe', 'pep440-git', '-'))

    assert e.value.args[0] == ('Could not transform version \'1.2.dev5-3-abcd123\''
                               if sys.version_info[0] == 3 else
                               'Could not transform version u\'1.2.dev5-3-abcd123\'')

def test_metadata_writer():
    command = fake_obj({ 
        'distribution': { 
            'metadata': { 
                'name': 'spam', 
                'version': '1.0' } }, 
        'write_or_delete_file': fake_func() })

    write_metadata_value(command, 'version.txt', 'spam.egg-info/version.txt')

    assert (('version', 'spam.egg-info/version.txt', '1.0'), { 'force': True }) \
           in command.write_or_delete_file.calls
