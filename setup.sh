#!/bin/bash
set -eu

cd $(dirname $0)

virtualenv env
./env/bin/pip install -r requirements.txt
./env/bin/python setup.py develop
