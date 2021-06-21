import codecs
import os
import sys

from setuptools import find_packages

if sys.version_info < (2, 3):
    raise RuntimeError("Python 2.3 or later is required")

from distutils.core import setup

here = os.path.abspath(os.path.dirname(__file__))


def get_version():
    import re

    with open("ergaster/version.py") as version_file:
        return re.search(
            r"""__version__\s+=\s+(['"])(?P<version>.+?)\1""", version_file.read()
        ).group("version")


def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


classifiers = [
    # "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.2",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Terminals",
    "Topic :: Utilities",
]

setup(
    name="ergaster",
    version=get_version(),
    author="Roman Vasilevsky",
    author_email="roman.vasilevsk@gmail.com",
    url="https://github.com/rvasilevsk/ergaster",
    license="MIT",
    description="ergaster package",
    long_description_content_type="text/markdown",
    long_description=readme(),
    platforms=["any"],
    python_requires=">=3.6",
    install_requires=[
        "pyperclip",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "erg = ergaster.cli:erg",
        ],
    },
    classifiers=classifiers,
    project_urls={
        "Bug Reports": "https://github.com/rvasilevsk/ergaster/issues",
        # "Read the Docs": "",
    },
    keywords=["cli", "clipboard"],
)
