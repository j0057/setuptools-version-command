import pytest

from setuptools_version_command import _parse_value

default = { 'post_ps': '.', 'post_t': 'post', 'post_is': '', 'post_im': '' }
implicit = { 'post_ps': '', 'post_t': '', 'post_is': '', 'post_im': '-' }

def test_str():
    assert _parse_value('git describe') == ('git describe', None, default)

def test_tuple_2():
    assert _parse_value(('git describe', 'pep440-git')) == ('git describe', 'pep440-git', default)

def test_tuple_2_wrong_pep440_mode():
    with pytest.raises(Exception) as e:
        _parse_value(('git describe', 'albatross'))
    assert e.value.args[0] == 'Unrecognized PEP440 mode \'albatross\''

def test_tuple_3():
    assert _parse_value(('git describe', 'pep440-git', '-')) == ('git describe', 'pep440-git', implicit)

def test_tuple_3_wrong_post_mode():
    with pytest.raises(Exception) as e:
        _parse_value(('git describe', 'pep440-git', '.whatever-'))
    assert e.value.args[0] == 'Unrecognized post mode \'.whatever-\''

def test_wrong_type():
    with pytest.raises(Exception) as e:
        _parse_value(13)
    assert e.value.args[0] == 'Unrecognized version_command value 13'
