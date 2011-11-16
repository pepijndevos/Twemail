#!/bin/bash

if [ ! -d bin ]
then
    virtualenv --no-site-packages .
fi

bin/pip install -r requirements.txt

echo "We're doing well. Please proceed"
