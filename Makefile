

venv: requirements.txt
	-rm -rf venv
	virtualenv venv ## expecting python3 by default
	venv/bin/python -m pip install -r requirements.txt

install: setup.py
	@echo "********* REMOVE AND REINSTALL PY PACKAGE *********"
	python setup.py clean --all && \
	pip install -e .

