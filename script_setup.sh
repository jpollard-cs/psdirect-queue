#!/bin/bash
[ ! -z $DEBUG ] && set -x


CWD=$(pwd)
cd $(dirname $0)/..
REPO_ROOT=$(pwd)
cd $CWD

PYTHON_VER=3.8.0
VIRTUAL_PY=venv.ps-direct
