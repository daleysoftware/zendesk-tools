#!/bin/bash
set -eu
cd "$(dirname $0)"
PYTHON="../../env/bin/python"
${PYTHON} delete-suspended-users.py $@