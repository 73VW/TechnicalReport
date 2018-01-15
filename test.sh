#!/bin/sh

set -xe

isort --recursive .
pycodestyle .
pydocstyle .
flake8 .
find . -iname "*.rst" | xargs rstcheck --report 2
