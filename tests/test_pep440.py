import pytest

from setuptools_version_command import _apply_pep440

pep440_git_local_cases = [
    ('1.0', '1.0'),
    ('1.0-1-abcd123', '1.0+git.1.abcd123')
]

pep440_git_dev_cases = [
    ('1.0', '1.0'),
    ('1.0-1-abcd123', '1.0.dev1')
]

pep440_none_cases = [
    ('1.0-1-abcd123', '1.0-1-abcd123')
]

pep440_git_cases = [
    # nodev nopost nopre
    ('1.2-0-abcd123', '1.2'),
    ('1.2-1-bcde234', '1.2.post1'),
    # nodev nopost openpre
    ('1.2a-0-abcd123', '1.2a0'),
    ('1.2a-1-bcde234', '1.2a1'),
    ('1.2.alpha-0-abcd123', '1.2.alpha0'),
    ('1.2.alpha-1-bcde234', '1.2.alpha1'),
    # nodev nopost closedpre
    ('1.2a0-0-abcd123', '1.2a0'),
    ('1.2a0-1-bcde234', '1.2a0.post1'),
    ('1.2a3-0-abcd123', '1.2a3'),
    ('1.2a3-1-bcde234', '1.2a3.post1'),
    # nodev openpost nopre
    ('1.2.post-0-abcd123', '1.2.post0'),
    ('1.2.post-1-bcde234', '1.2.post1'),
    # nodev openpost openpre
    ('1.2a.post-0-abcd123', '1.2a0.post0'), 
    ('1.2a.post-1-bcde234', '1.2a0.post1'),
    # nodev openpost closedpre
    ('1.2a0.post-0-abcd123', '1.2a0.post0'),
    ('1.2a0.post-1-bcde234', '1.2a0.post1'),
    ('1.2a3.post-0-abcd123', '1.2a3.post0'),
    ('1.2a3.post-1-bcde234', '1.2a3.post1'),
    # nodev closedpost nopre
    ('1.2.post0-0-abcd123', '1.2.post0'),
    ('1.2.post0-1-bcde234', None),
    ('1.2.post4-0-abcd123', '1.2.post4'),
    ('1.2.post4-1-bcde234', None),
    # nodev closedpost openpre
    ('1.2a.post0-0-abcd123', '1.2a0.post0'),
    ('1.2a.post0-1-bcde234', None),
    ('1.2a.post4-0-abcd123', '1.2a0.post4'),
    ('1.2a.post4-1-bcde234', None),
    # nodev closedpost closedpre
    ('1.2a0.post0-0-abcd123', '1.2a0.post0'),
    ('1.2a0.post0-1-bcde234', None),
    ('1.2a0.post4-0-abcd123', '1.2a0.post4'),
    ('1.2a0.post4-1-bcde234', None),
    ('1.2a3.post4-0-abcd123', '1.2a3.post4'),
    ('1.2a3.post4-1-bcde234', None),

    # opendev nopost nopre
    ('1.2.dev-0-abcd123', '1.2.dev0'),
    ('1.2.dev-1-bcde234', '1.2.dev1'),
    # opendev nopost openpre
    ('1.2a.dev-0-abcd123', '1.2a0.dev0'),
    ('1.2a.dev-1-bcde234', '1.2a0.dev1'),
    # opendev nopost closedpre
    ('1.2a0.dev-0-abcd123', '1.2a0.dev0'),
    ('1.2a0.dev-1-bcde234', '1.2a0.dev1'),
    ('1.2a3.dev-0-abcd123', '1.2a3.dev0'),
    ('1.2a3.dev-1-bcde234', '1.2a3.dev1'),
    # opendev openpost nopre
    ('1.2.post.dev-0-abcd123', '1.2.post0.dev0'),
    ('1.2.post.dev-1-bcde234', '1.2.post0.dev1'),
    # opendev openpost openpre
    ('1.2a.post.dev-0-abcd123', '1.2a0.post0.dev0'),
    ('1.2a.post.dev-1-bcde234', '1.2a0.post0.dev1'),
    # opendev openpost closedpre
    ('1.2a0.post.dev-0-abcd123', '1.2a0.post0.dev0'),
    ('1.2a0.post.dev-1-bcde234', '1.2a0.post0.dev1'),
    ('1.2a3.post.dev-0-abcd123', '1.2a3.post0.dev0'),
    ('1.2a3.post.dev-1-bcde234', '1.2a3.post0.dev1'),
    # opendev closedpost nopre
    ('1.2.post0.dev-0-abcd123', '1.2.post0.dev0'),
    ('1.2.post0.dev-1-bcde234', '1.2.post0.dev1'),
    ('1.2.post4.dev-0-abcd123', '1.2.post4.dev0'),
    ('1.2.post4.dev-1-bcde234', '1.2.post4.dev1'),
    # opendev closedpost openpre
    ('1.2a.post0.dev-0-abcd123', '1.2a0.post0.dev0'),
    ('1.2a.post0.dev-1-bcde234', '1.2a0.post0.dev1'),
    ('1.2a.post4.dev-0-abcd123', '1.2a0.post4.dev0'),
    ('1.2a.post4.dev-1-bcde234', '1.2a0.post4.dev1'),
    # opendev closedpost closedpre
    ('1.2a0.post0.dev-0-abcd123', '1.2a0.post0.dev0'),
    ('1.2a0.post0.dev-1-bcde234', '1.2a0.post0.dev1'),
    ('1.2a0.post4.dev-0-abcd123', '1.2a0.post4.dev0'),
    ('1.2a0.post4.dev-1-bcde234', '1.2a0.post4.dev1'),
    ('1.2a3.post4.dev-0-abcd123', '1.2a3.post4.dev0'),
    ('1.2a3.post4.dev-1-bcde234', '1.2a3.post4.dev1'),

    # closeddev nopost nopre
    ('1.2.dev0-0-abcd123', '1.2.dev0'),
    ('1.2.dev0-1-bcde234', None),
    ('1.2.dev5-0-abcd123', '1.2.dev5'),
    ('1.2.dev5-1-bcde234', None),
    # closeddev nopost openpre
    ('1.2a.dev0-0-abcd123', '1.2a0.dev0'),
    ('1.2a.dev0-1-bcde234', None),
    ('1.2a.dev5-0-abcd123', '1.2a0.dev5'),
    ('1.2a.dev5-1-bcde234', None),
    # closeddev nopost closedpre
    ('1.2a0.dev0-0-abcd123', '1.2a0.dev0'),
    ('1.2a0.dev0-1-bcde234', None),
    ('1.2a3.dev0-0-abcd123', '1.2a3.dev0'),
    ('1.2a3.dev0-1-bcde234', None),
    ('1.2a3.dev5-0-abcd123', '1.2a3.dev5'),
    ('1.2a3.dev5-1-bcde234', None),
    # closeddev openpost nopre
    ('1.2.post.dev0-0-abcd123', '1.2.post0.dev0'),
    ('1.2.post.dev0-1-bcde234', None),
    ('1.2.post.dev5-0-abcd123', '1.2.post0.dev5'),
    ('1.2.post.dev5-1-bcde234', None),
    # closeddev openpost openpre
    ('1.2a.post.dev0-0-abcd123', '1.2a0.post0.dev0'),
    ('1.2a.post.dev0-1-bcde234', None),
    ('1.2a.post.dev5-0-abcd123', '1.2a0.post0.dev5'),
    ('1.2a.post.dev5-1-bcde234', None),
    # closeddev openpost closedpre
    ('1.2a0.post.dev0-0-abcd123', '1.2a0.post0.dev0'),
    ('1.2a0.post.dev0-1-bcde234', None),
    ('1.2a3.post.dev0-0-abcd123', '1.2a3.post0.dev0'),
    ('1.2a3.post.dev0-1-bcde234', None),
    ('1.2a3.post.dev5-0-abcd123', '1.2a3.post0.dev5'),
    ('1.2a3.post.dev5-1-bcde234', None),
    # closeddev closedpost nopre
    ('1.2.post0.dev0-0-abcd123', '1.2.post0.dev0'),
    ('1.2.post0.dev0-1-bcde234', None),
    ('1.2.post4.dev0-0-abcd123', '1.2.post4.dev0'),
    ('1.2.post4.dev0-1-bcde234', None),
    ('1.2.post4.dev5-0-abcd123', '1.2.post4.dev5'),
    ('1.2.post4.dev5-1-bcde234', None),
    # closeddev closedpost openpre
    ('1.2a.post0.dev0-0-abcd123', '1.2a0.post0.dev0'),
    ('1.2a.post0.dev0-1-bcde234', None),
    ('1.2a.post4.dev0-0-abcd123', '1.2a0.post4.dev0'),
    ('1.2a.post4.dev0-1-bcde234', None),
    ('1.2a.post4.dev5-0-abcd123', '1.2a0.post4.dev5'),
    ('1.2a.post4.dev5-1-bcde234', None),
    # closeddev closedpost closedpre
    ('1.2a0.post0.dev0-0-abcd123', '1.2a0.post0.dev0'),
    ('1.2a0.post0.dev0-1-bcde234', None),
    ('1.2a3.post0.dev0-0-abcd123', '1.2a3.post0.dev0'),
    ('1.2a3.post0.dev0-1-bcde234', None),
    ('1.2a0.post4.dev0-0-abcd123', '1.2a0.post4.dev0'),
    ('1.2a0.post4.dev0-1-bcde234', None),
    ('1.2a3.post4.dev0-0-abcd123', '1.2a3.post4.dev0'),
    ('1.2a3.post4.dev0-1-bcde234', None),
    ('1.2a0.post0.dev5-0-abcd123', '1.2a0.post0.dev5'),
    ('1.2a0.post0.dev5-1-bcde234', None),
    ('1.2a3.post0.dev5-0-abcd123', '1.2a3.post0.dev5'),
    ('1.2a3.post0.dev5-1-bcde234', None),
    ('1.2a0.post4.dev5-0-abcd123', '1.2a0.post4.dev5'),
    ('1.2a0.post4.dev5-1-bcde234', None),
    ('1.2a3.post4.dev5-0-abcd123', '1.2a3.post4.dev5'),
    ('1.2a3.post4.dev5-1-bcde234', None),
]

#pply_pep440_wrong_mode = lambda v: _apply_pep440(v, 'albatross')
#pply_pep440_git_local = lambda v: _apply_pep440(v, 'pep440-git-local')
#pply_pep440_git_dev = lambda v: _apply_pep440(v, 'pep440-git-dev')
#pply_pep440_none = lambda v: _apply_pep440(v, None)
#pply_pep440 = lambda v: _apply_pep440(v, 'pep440-git')
apply_pep440_implicit_post = lambda v: _apply_pep440(v, 'pep440-git', pep440_post={'post_im': '-'})

def test_wrong_mode():
    with pytest.raises(Exception) as e:
        _apply_pep440('1.0', 'albatross')
    assert e.value.args[0] == "Unrecognized PEP440 mode 'albatross'"

@pytest.mark.parametrize(('describe', 'expected'), pep440_git_local_cases)
def test_pep440_git_local(describe, expected):
    assert _apply_pep440(describe, 'pep440-git-local') == expected

@pytest.mark.parametrize(('describe', 'expected'), pep440_git_dev_cases)
def test_pep440_git_dev(describe, expected):
    assert _apply_pep440(describe, 'pep440-git-dev')

@pytest.mark.parametrize(('describe', 'expected'), pep440_none_cases)
def test_pep440_none(describe, expected):
    assert _apply_pep440(describe, None) == expected

def test_pep440_git_nodev_nopost_nopre__implicit_post():
    assert apply_pep440_implicit_post('1.2-0-abcd123') == '1.2'
    assert apply_pep440_implicit_post('1.2-1-bcde234') == '1.2-1'
    assert apply_pep440_implicit_post('1.2-9-g91941b4') == '1.2-9'

@pytest.mark.parametrize(('describe', 'result'), pep440_git_cases)
def test_pep440_git(describe, result):
    assert _apply_pep440(describe, 'pep440-git') == result
