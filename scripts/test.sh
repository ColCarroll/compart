#! /bin/bash

set -ex # fail on first error, print commands

SRC_DIR=${SRC_DIR:-$(pwd)}

python -m pytest -xv --cov "${SRC_DIR}"/compart --cov-report=html "${SRC_DIR}"/test
