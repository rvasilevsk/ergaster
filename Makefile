TEST_PATH=./
PKG_SRC=./src/ergaster
#PYTHON_PATH=./src/

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
	pip install -U dist/ergaster-0.0.1-py3-none-any.whl
	python -c "from ergaster.ergaster import main; main()"
	pip uninstall -y ergaster

docs:
	pdoc3 --html -o docs -f src/ergaster
	#cp logo.png docs/

live:
	# TODO ModuleNotFoundError: spec not found for the module 'ergaster'
	pdoc3 --http : ergaster bench

build:
	python -m pip install --upgrade build
	python -m build
	echo > _build.pyc

clean: clean-pyc clean-build clean-docs

clean-pyc:
	rm -r *.pyc  *.pyo

clean-build:
	rm -r build dist *.egg-info

clean-docs:
	rm -r docs

lint:
	flake8 --exclude=venv,.tox,.git,__pycache__,docs,old,build,dist

black:
	black --check --diff ./src/ergaster ./tests

black-fix: _black-fix.pyc

_black-fix.pyc: src/ergaster tests
	black ./src/ergaster ./tests
	echo > _black-fix.pyc

isort:
	isort --check-only --diff ./src/ergaster ./tests

isort-fix:
	isort ./src/ergaster ./tests

fix: isort-fix black-fix

pytest:
	pytest --verbose --color=yes

.PHONY: tests docs build
