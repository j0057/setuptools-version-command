import os
import os.path
import re
import subprocess

# see pep440-version-regex.png
_PEP440_VERSION = re.compile(r'^(?P<v>v)?(?:(?P<e>\d+)(?P<e_s>!))?(?P<r>\d+(?:\.\d+)*)(?:(?P<pre_ps>[\._-])?(?P<pre_t>a|alpha|b|beta|rc|c|pre|preview)(?P<pre_is>[\._-](?=\d))?(?P<pre_n>\d*))?(?:(?:(?P<post_ps>[\._-])?(?P<post_t>post|rev|r)(?P<post_is>[\._-](?=\d))?|(?P<post_im>-))(?P<post_n>(?(post_t)\d*|\d+)))?(?:(?P<dev_ps>[\._-])?(?P<dev_t>dev)(?P<dev_is>[\._-](?=\d))?(?P<dev_n>\d*))?(?:-(?P<git_rev>\d+)-(?P<git_commit>g?[0-9a-f]{4,20}))?$', re.IGNORECASE|re.VERBOSE)
_PEP440_POST_MODE = re.compile(r'^(?:(?P<post_ps>[\._-]?)(?P<post_t>post|rev|r)(?P<post_is>[\._-]?)|(?P<post_im>-))?$')

def validate_version_command_keyword(dist, attr, value):
    egg_info_dir = dist.metadata.name.replace('-', '_') + '.egg-info'

    version_txt      = egg_info_dir + '/version.txt'
    version_full_txt = egg_info_dir + '/version_full.txt'

    (command, pep440_mode, pep440_post) = _parse_value(value)

    (current_short_version, current_full_version) = _get_scm_version(command, pep440_mode, pep440_post)
    (cached_short_version, cached_full_version) = _get_cached_version(version_txt, version_full_txt)

    if current_short_version:
        dist.metadata.version = current_short_version
        dist.metadata.version_full = current_full_version
    elif cached_short_version:
        dist.metadata.version = cached_short_version
        dist.metadata.version_full = cached_full_version
    else:
        raise Exception('Could not find version from {0!r} or from {1}'.format(command, version_full_txt))

def write_metadata_value(command, basename, filename):
    attr_name = os.path.splitext(basename)[0]
    attr_value = getattr(command.distribution.metadata, attr_name) \
                 if hasattr(command.distribution.metadata, attr_name) \
                 else None
    command.write_or_delete_file(attr_name, filename, attr_value, force=True)

def _parse_value(value):
    if isinstance(value, str):
        value = (value, None)

    if isinstance(value, tuple) and len(value) == 2:
        value = value + ('.post',)

    if isinstance(value, tuple) and len(value) == 3:
        if value[0] not in ['git describe', 'git describe --long']:
            raise Exception('Unsupported SCM command {0!r}'.format(value[0]))

        if value[1] is None:
            pass
        elif value[1] in ['pep440-git', 'pep440-git-dev', 'pep440-git-local']:
            pass
        else:
            raise Exception('Unrecognized PEP440 mode {0!r}'.format(value[1]))

        (command, pep440_mode, pep440_post) = value
        match = _PEP440_POST_MODE.match(pep440_post)
        if not match:
            raise Exception('Unrecognized post mode {0!r}'.format(value[2]))
        pep440_post_mode = { k: v or '' for (k, v) in match.groupdict().items() }

        return (command, pep440_mode, pep440_post_mode)

    else:
        raise Exception('Unrecognized version_command value {0!r}'.format(value))

def _get_scm_version(command, pep440_mode, pep440_post):
    try:
        cmd = command.split()
        full_version = subprocess.check_output(cmd).strip()
    except:
        full_version = None

    if full_version:
        short_version = _apply_pep440(full_version, pep440_mode, pep440_post)
        if not short_version:
            raise Exception('Could not transform version {0!r}'.format(full_version))
    else:
        short_version = None

    return (short_version, full_version)

def _get_cached_version(version_txt, version_full_txt):
    return (_read_version(version_txt), _read_version(version_full_txt))

def _read_version(filename):
    try:
        with open(filename, 'r') as f:
            return f.read()
    except:
        return None

def _split_version(version):
    match = _PEP440_VERSION.match(version)
    if not match:
        raise Exception('Can\'t parse version {0!r} as PEP440 version'.format(version))
    return { k: v or '' for (k, v) in match.groupdict().items() }

def _join_version(v):
    return '{v}{e}{e_s}{r}{pre_ps}{pre_t}{pre_is}{pre_n}{post_ps}{post_t}{post_is}{post_im}{post_n}{dev_ps}{dev_t}{dev_is}{dev_n}'.format(**v)

def _apply_pep440(version, pep440_mode, pep440_post={'post_ps':'.', 'post_t': 'post', 'post_is': '', 'post_im': ''}):
    if pep440_mode in ['pep440-git-local']:
        return version.replace('-', '+git-', 1).replace('-', '.')

    elif pep440_mode in ['pep440-git-dev']:
        # XXX: This is not compliant with PEP440. It is supported here for backwards-compatibility
        if '-' in version:
            parts = version.split('-')
            parts[-2] = 'dev' + parts[-2]
            return '.'.join(parts[:-1])
        else:
            return version

    elif pep440_mode in ['pep440-git']:
        vd = _split_version(version)
        revs = vd['git_rev'] or '0'

        # on git tag, so don't do anything
        if revs == 'x':
            pass
        # has dev tag, update number if it's implicitly 0
        elif vd['dev_t']:
            if vd['dev_n'] == '':
                vd['dev_n'] = revs
            elif revs != '0':
                return None
        # has post tag, update number if it's implicitly 0
        elif vd['post_t'] or vd['post_im']:
            if vd['post_n'] == '':
                vd['post_n'] = revs
            elif revs != '0':
                return None
        else:
            # update pre tag if it's implicitly 0
            if vd['pre_t'] and (vd['pre_n'] == ''):
                vd['pre_n'] = revs
            # else add a post tag
            elif revs != '0':
                vd.update(pep440_post)
                vd['post_n'] = revs

        if vd['pre_t'] and not vd['pre_n']: vd['pre_n'] = '0'
        if (vd['post_t'] or vd['post_im']) and not vd['post_n']: vd['post_n'] = '0'
        if vd['dev_t'] and not vd['dev_n']: vd['dev_n'] = '0'

        return _join_version(vd)

    elif pep440_mode is None:
        return version

    else:
        raise Exception('Unrecognized PEP440 mode {0!r}'.format(pep440_mode))
