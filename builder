#!/bin/bash

if [ ! -d ~/bin ]
then
    echo "no virtaulenv yet"
    virtualenv --no-site-packages ~
fi

~/bin/pip install -r requirements.txt

pwd
echo "copy ourselves"
cp -a . ~
echo "We're doing well. Please proceed"
