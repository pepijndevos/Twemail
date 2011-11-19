#!/bin/bash
CODEROOT="$PWD"
cd "$(dirname "$0")"
rm ~/profile

PYTHON=python$SERVICE_ENVIRONMENT_PYTHON_VERSION
echo -n "Looking for Python interpreter ($PYTHON): "
which $PYTHON || {
    echo "not found, aborting."
    exit 1
}
[ -d ~/virtualenv ] ||
    virtualenv --python=$PYTHON ~/virtualenv
. ~/virtualenv/bin/activate
echo '. ~/virtualenv/bin/activate' >>~/profile

cd "$CODEROOT/$SERVICE_APPROOT"
[ -f requirements.txt ] &&
    pip install --download-cache=~/.pip-cache -r requirements.txt
if [ -f setup.py ]
then
    pip install .
else
    cp -a . ~
    echo 'export PYTHONPATH=~' >>~/profile
fi
