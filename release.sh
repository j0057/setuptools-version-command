#!/bin/bash -x

DIST_DIR="/tmp/pypkg27"

VERSION="$(./setup.py --version)"
DIST_NAME="setuptools-version-command"

./setup.py sdist --dist-dir=$DIST_DIR
pip wheel --no-index --find-links=$DIST_DIR --wheel-dir=$DIST_DIR "$DIST_NAME==$VERSION"
sudo pip install --upgrade --no-index --find-links=$DIST_DIR --use-wheel "$DIST_NAME==$VERSION"
