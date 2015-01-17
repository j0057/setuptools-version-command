import os
import os.path
import subprocess
import sys

import distutils.core

# setup(
#   version_command='git describe',
#   version_command_pep440='git'
#   ...)

def execute_version_command(dist, attr, value):
    filename = dist.metadata.name + '.egg-info/version.txt'
    version = get_scm_version(filename, value, pep440=dist.metadata.version_pep440)
    dist.metadata.version = version

def set_pep440(dist, attr, value):
    dist.metadata.version_pep440 = value
    
def get_scm_version(filename, command, pep440 = None):
    # get version 
    try:
        cmd = command.split()
        scm_version = subprocess.check_output(cmd).strip()
    except:
        scm_version = None

    # apply pep440 if requested
    scm_version = apply_pep440(pep440, scm_version)

    # also get version from distname.egg-info/version.txt
    try:
        with open(filename, 'r') as f:
            cached_version = f.read().strip()
    except:
        cached_version = None

    # at least one of the two should succeed
    if not (scm_version or cached_version):
        raise Exception('Could not find version from {0!r} or from {1}'.format(command, filename))

    # if the cached version is wrong
    if scm_version and (scm_version != cached_version):

        # create directory if necessary
        dirname = os.path.dirname(filename)
        if not os.path.isdir(dirname):
            os.makedirs(dirname)

        # rewrite cached version
        with open(filename, 'w') as f:
            f.write(scm_version)
        return scm_version

    # there is only the cached version or it doesn't matter
    else:
        return cached_version

def apply_pep440(mode, version):
    if mode in ['git', 'git-local']:
        return version.replace('-', '+git-', 1).replace('-', '.')

    elif mode == 'git-dev':
        parts = version.split('-')
        parts[-2] = 'dev' + parts[-2]
        return '.'.join(parts[:-1])

    elif mode == None:
        return version

    else:
        raise Exception('Unrecognized mode {0!r}'.format(mode))
