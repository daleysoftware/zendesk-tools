#!/bin/bash
set -eu

cd $(dirname $0)

virtualenv -p $(which python3) env
./env/bin/pip install -r requirements.txt
./env/bin/python setup.py develop
