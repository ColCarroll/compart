#! /bin/bash

set -ex # fail on first error, print commands

SRC_DIR=${SRC_DIR:-$(pwd)}

echo "Checking documentation..."
python -m pydocstyle --convention=numpy "${SRC_DIR}"/compart/
echo "Success!"

echo "Checking code style with black..."
python -m black --check "${SRC_DIR}"/compart/ "${SRC_DIR}"/test/
echo "Success!"

echo "Checking types mypy..."
python -m mypy --ignore-missing-imports "${SRC_DIR}"/compart/ "${SRC_DIR}"/test/
echo "Success!"


echo "Checking code style with pylint..."
python -m pylint "${SRC_DIR}"/compart/
echo "Success!"
