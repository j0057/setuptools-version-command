setuptools-version-command 
==========================

*Get version from version control instead of hardcoding it into setup.py*

introduction
------------

Instead of hardcoding the version in ``setup.py`` like this:

.. code-block:: python

    setup(
        name='some-dist-name',
        version='1.0',
        ...)

This package allows specifying a VCS command like this:

.. code-block:: python

    setup(
        name='some-dist-name',
        version_command='git describe',
        ...)

...Which will then update the version into
``some-dist-name.egg-info/version.txt``, so that the version can also be found
if ``setup.py`` is being run from an sdist or something.

When it can find the version from either
``some-dist-name.egg-info/version.txt`` or the output of the
``version_command``, it will update the version key that is normally used for
the version, such as what's used in the sdist filename and so on.

setup keyword
-------------

Instead of specifying the ``version`` keyword argument, specify the
``version_command`` keyword argument. It can either be a str or a tuple. If
it's a str, it's interpreted as just the command to execute, for example ``git
describe``. If it's a tuple, it must have two or three elements, and have the
form ``(command, pep440_mode[, post_mode])``. 

:``command``: Must be ``"git describe"``, but could also support other VCS in
    the future.

:``pep440_mode`` = ``None``: Takes output of command as is, so ignores PEP440.
    ``pip`` and ``setuptools`` will throw warnings.

:``pep440_mode`` = ``"pep440-git-local"``: Moves number of commits and hash as
    local identifier:

    * Change ``1.2.3`` to ``1.2.3``
    * Change ``1.2.3-10-abc1234`` to ``1.2.3+git-10-abc1234``

:``pep440_mode`` = ``"pep440-git-dev"``: (Deprecated) Adds rhe number of
    commits since a git tag as a .dev tag:

    * Change ``1.2.3-N-abc1234`` to ``1.2.3.devN``

    This is against PEP440-specification and supported only for backwards
    compatibility. It may be removed in time.

:``pep440_mode`` = ``"pep440-git"``: Works with pre-release versions (alpha,
    beta, rc etc), post-release versions (post, rev, etc) and dev versions.

    * Leave ``1.2.3.dev`` and ``1.2.3.dev0`` as they are
    * Change ``1.2.3.dev-N-abc1234`` to ``1.2.3.devN``
    * Change ``1.2.3a-N-ab1234`` to ``1.2.3aN``
    * Change ``1.2.3`` to ``1.2.3``
    * Change ``1.2.3-10-abcd123`` to ``1.2.3.post10``, or ``1.2.3-rev10``, as
      you prefer

    In other words, a tag can be absent, open (implicitly or explicitly 0), or
    closed (have a number greater than zero). If the last Git tag is an open
    dev tag, that's the one that will be used for the revision number. If the
    last Git tag is an open post-release tag, then that will be used. If the
    last Git tag is an open pre-release tag, that will be used. In other cases,
    a post-release tag will be added. 

:``post_mode``: Template for adding post-release tags. Optional separator (dot,
    dash or underscore), followed by ``"post"``, ``"rev"`` or ``"r"``, followed
    by another optional separator. Can also be a single dash. Default is
    ``".post"``.

    Given a git describe output of ``1.2a3-4-abcd123``:

    * ``".post"`` gives ``1.2a3.post4``
    * ``".rev_"`` gives ``1.2a3.rev_4``
    * ``"-"`` gives ``1.2a3-4``

installation
------------

To use it, just do this:

.. code-block:: shell

    pip install setuptools-version-command

With the pip of the global python. (Or use ``--user``.)

testing
-------

To test it, run ``./setup.py --version``.

developing
----------

Within a checkout of this repo:

.. code-block:: shell

    virtualenv env
    env/bin/pip install --editable .
    env/bin/python setup.py --version

Make sure that you change the ``setup.py`` so that it actually makes use of
setuptools-version-command.
