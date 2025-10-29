


# Cleaning up development environment
.PHONY: clean
clean:
	-rm -rf dist *.egg-info */__pycache__

# Using python -m venv .venv to make be found by positron
venv: requirements.txt
	-rm -rf .venv
	python3 -m virtualenv .venv
	.venv/bin/python -m pip install -r requirements.txt
	.venv/bin/python -m pip install --upgrade pip build twine setuptools wheel

install: setup.py
	@echo "********* REMOVE AND REINSTALL PY PACKAGE (developer version) *********"
	python setup.py clean --all && \
	python -m pip install -e .

# Prepare package for PyPI submission
.PHONY: build
build: clean
	-rm -rf build dist *.egg-info
	python -m build

# Rules to push releases to PyPI test and PyPI.
# Makes use of the token/config stored in $HOME/.pypirc

testpypi: build
	twine check dist/*
	twine upload --verbose --repository testpypi dist/*

pypirelease: build
	twine check dist/*
	twine upload --verbose --repository pypi dist/*
