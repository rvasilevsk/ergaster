TEST_PATH=./
PKG_SRC=./src/ergaster
#PYTHON_PATH=./src/
PY_FILES=setup.py ./ergaster ./tests

default: pytest

.PHONY: all
all: docs tests dist

venv:
	python -m venv venv

.PHONY: freeze
freeze:
	pip freeze

.PHONY: requirements
requirements: venv _requirements.txt.pyc _requirements-test.txt.pyc

_requirements.txt.pyc: requirements.txt
#	.\venv\Scripts\activate.bat
	#pip install -r --upgrade requirements.txt
	pip install -r requirements.txt
	echo > _requirements.txt.pyc

_requirements-test.txt.pyc: requirements-test.txt
#	.\venv\Scripts\activate.bat
	pip install -r requirements-test.txt
	echo > _requirements-test.txt.pyc

.PHONY: whl-test
whl-test:
	pip uninstall -y ergaster
	pip install -U dist/ergaster-0.0.2-py3-none-any.whl
	pip show -f ergaster
	python -c "from ergaster import main; main()"
	erg
	pip uninstall -y ergaster

.PHONY: docs
docs:
	pdoc3 --html -o docs -f ergaster pyperclip
	#cp logo.png docs/

.PHONY: live
live:
	# TODO ModuleNotFoundError: spec not found for the module 'ergaster'
	pdoc3 --http : ergaster bench

.PHONY: build
build: clean-build
	python -m pip install --upgrade build
	python -m build
	echo > _build.pyc

.PHONY: upload
upload:
	python -m twine upload --repository testpypi dist/*
	echo to install: python -m pip install --index-url https://test.pypi.org/simple/ ergaster

.PHONY: clean
clean: clean-pyc clean-build clean-docs

.PHONY: clean-pyc
clean-pyc:
	rm -rf *.pyc *.pyo ergaster/__pycache__ tests/__pycache__

.PHONY: clean-build
clean-build:
	rm -rf build dist *.egg-info

.PHONY: clean-docs
clean-docs:
	rm -rf docs

.PHONY: lint
lint:
	flake8 --exclude=venv,.tox,.git,__pycache__,docs,old,build,dist

.PHONY: black
black:
	black --check --diff $(PY_FILES)

black-fix: _black-fix.pyc

_black-fix.pyc: ergaster tests
	black $(PY_FILES)
	echo > _black-fix.pyc

.PHONY: isort
isort:
	isort --check-only --diff $(PY_FILES)

.PHONY: isort-fix
isort-fix:
	isort $(PY_FILES)

.PHONY: fix
fix: isort-fix black-fix

.PHONY: pytest
pytest:
	PYTHONPATH=.
	pytest --verbose --color=yes
