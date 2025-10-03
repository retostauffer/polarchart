


# Cleaning up development environment
clean:
	-rm -rf dist *.egg-info */__pycache__

# Using python -m venv .venv to make be found by positron
venv: requirements.txt
	-rm -rf venv
	python3 -m venv .venv
	.venv/bin/python -m pip install -r requirements.txt

install: setup.py
	@echo "********* REMOVE AND REINSTALL PY PACKAGE (developer version) *********"
	python setup.py clean --all && \
	python -m pip install -e .

# Prepare package for PyPI submission
sdist:
	-rm -rf dist
	python setup.py sdist

wheel:
	python setup.py bdist_wheel --universal

# Rules to push releases to PyPI test and PyPI.
# Makes use of the token/config stored in $HOME/.pypirc

testpypi:
	make sdist
	twine upload --verbose --repository testpypi dist/*

pypirelease:
	make sdist
	twine upload --verbose --repository pypi dist/*
