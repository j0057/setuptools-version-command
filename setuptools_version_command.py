import os
import os.path
import subprocess

# version_command=('git describe', 'pep440-git-dev')
# version_command=('git describe', 'pep440-git-local')
# version_command=('git describe', 'pep440-git')
# version_command=('git describe', None)
# version_command='git describe'

def validate_version_command_keyword(dist, attr, value):
    egg_info_dir = dist.metadata.name.replace('-', '_') + '.egg-info'

    version_txt      = egg_info_dir + '/version.txt'
    version_full_txt = egg_info_dir + '/version_full.txt'

    (command, pep440_mode) = _parse_value(value)

    current_short_version, current_full_version = _get_scm_version(command, pep440_mode)
    cached_short_version, cached_full_version = _get_cached_version(version_txt, version_full_txt)

    if not (current_full_version or cached_full_version):
        raise Exception('Could not find version from {0!r} or from {1}'.format(command, version_full_txt))

    dist.metadata.version = current_short_version or cached_short_version
    dist.metadata.version_full = current_full_version or cached_full_version

def write_metadata_value(command, basename, filename):
    attr_name = os.path.splitext(basename)[0]
    attr_value = getattr(command.distribution.metadata, attr_name) \
                 if hasattr(command.distribution.metadata, attr_name) \
                 else None
    command.write_or_delete_file(attr_name, filename, attr_value, force=True)

def _parse_value(value):
    if isinstance(value, str):
        return (value, None)

    elif isinstance(value, tuple) and len(value) == 2:

        if value[0] not in ['git describe']:
            raise Exception('Unsupported SCM command {0!r}'.format(value))

        if value[1] is None:
            pass
        elif value[1] in ['pep440-git', 'pep440-git-dev', 'pep440-git-local']:
            pass
        else:
            raise Exception ('Unrecognized value {0!r}', value[1])

        return value

    else:
        raise Exception('Unrecognized value {0!r}'.format(value))

def _get_scm_version(command, pep440_mode):
    try:
        cmd = command.split()
        full_version = subprocess.check_output(cmd).strip()
    except:
        full_version = None

    if full_version:
        short_version = _apply_pep440(full_version, pep440_mode)
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

def _apply_pep440(version, mode):
    if mode in ['pep440-git-local']:
        return version.replace('-', '+git-', 1).replace('-', '.')

    elif mode in ['pep440-git', 'pep440-git-dev']:
        if '-' in version:
            parts = version.split('-')
            parts[-2] = 'dev' + parts[-2]
            return '.'.join(parts[:-1])
        else:
            return version

    elif mode == None:
        return version

    else:
        raise Exception('Unrecognized mode {0!r}'.format(mode))
