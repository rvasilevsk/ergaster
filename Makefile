TEST_PATH=./
PKG_SRC=./src/ergaster
#PYTHON_PATH=./src/
PY_FILES=setup.py ./ergaster ./tests

all: docs tests dist

venv:
	python -m venv venv

freeze:
	pip freeze

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

whl-test:
	pip uninstall -y ergaster
	pip install -U dist/ergaster-0.0.2-py3-none-any.whl
	pip show -f ergaster
	python -c "from ergaster import main; main()"
	erg
	pip uninstall -y ergaster

docs:
	pdoc3 --html -o docs -f src/ergaster
	#cp logo.png docs/

live:
	# TODO ModuleNotFoundError: spec not found for the module 'ergaster'
	pdoc3 --http : ergaster bench

build: clean-build
	python -m pip install --upgrade build
	python -m build
	echo > _build.pyc

upload:
	python -m twine upload --repository testpypi dist/*
	echo to install: python -m pip install --index-url https://test.pypi.org/simple/ ergaster

clean: clean-pyc clean-build clean-docs

clean-pyc:
	rm -rf *.pyc *.pyo ergaster/__pycache__ tests/__pycache__

clean-build:
	rm -rf build dist *.egg-info

clean-docs:
	rm -rf docs

lint:
	flake8 --exclude=venv,.tox,.git,__pycache__,docs,old,build,dist

black:
	black --check --diff $(PY_FILES)

black-fix: _black-fix.pyc

_black-fix.pyc: ergaster tests
	black $(PY_FILES)
	echo > _black-fix.pyc

isort:
	isort --check-only --diff $(PY_FILES)

isort-fix:
	isort $(PY_FILES)

fix: isort-fix black-fix

pytest:
	pytest --verbose --color=yes

#.PHONY: tests docs build
