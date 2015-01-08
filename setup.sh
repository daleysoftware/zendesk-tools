#!/bin/bash
set -eu

cd $(dirname $0)

virtualenv env
./env/bin/python setup.py develop
