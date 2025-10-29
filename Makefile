


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

# Create man pages (_quarto/man/*.qmd) by extracting docstrings
# from python classes and functions. Requires pyp2qmd to be installed.
# - https://github.com/retostauffer/pyp2qmd
document:
	@echo "********* CREATE (OVERWRITE) QMD FILES ************"
	pyp2qmd document --package polarchart

# Uses `pyp2qmd` to extract all examples from the docstrings, and
# creates a series of quarto markdown files (qmd). Used for testing
# that the examples work as expected.
# - https://github.com/retostauffer/pyp2qmd
examples:
	@echo "********* CREATE (EXAMPLES) QMD FILES *************"
	rm -rf _examples
	pyp2qmd examples --package colorspace
	cd _examples && for file in *.qmd; do quarto render $$file || exit 99; done


# Render documentation. Requires quarto to be installed as well
# a series of python packages used in the documentation (see
# requirements_devel.txt; make venv).
# - https://quarto.org/
render:
	@echo "********* RENDERING QUARTO WEBSITE ****************"
	(make document && cd _quarto && quarto render)

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
