#!/bin/sh
rm -rf dist build
python setup.py bdist_wheel
twine upload -r pypi dist/*
