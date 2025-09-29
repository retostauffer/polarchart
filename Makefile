

venv: requirements.txt
	-rm -rf venv
	virtualenv venv ## expecting python3 by default
	venv/bin/python -m pip install -r requirements.txt

install: setup.py
	@echo "********* REMOVE AND REINSTALL PY PACKAGE *********"
	python setup.py clean --all && \
	pip install -e .

# Prepare package for PyPI submission
sdist:
	-rm -rf dist
	python setup.py sdist

# Rules to push releases to PyPI test and PyPI.
# Makes use of the token/config stored in $HOME/.pypirc

testpypi:
	make sdist
	twine upload --verbose --repository testpypi dist/*

pypirelease:
	make sdist
	twine upload --verbose --repository pypi dist/*
