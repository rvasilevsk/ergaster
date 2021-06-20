# Ergaster


The **ergaster** module provides none functions to do nothing, yet.

[rvasilevsk/ergaster](https://github.com/rvasilevsk/ergaster)

## Prerequisites

Python 2.3 (TODO) or later.

## Installation

### Installing With pip

The easiest way to install the latest version of the module is to use the `pip` tool:

```
$ pip install --index-url https://test.pypi.org/simple/ ergaster
```

```
$ pip install --upgrade https://github.com/rvasilevsk/ergaster/tarball/master
```
### Installing From Source

Alternatively, you can install the module from the source distribution. The steps below will guide you through the process.


 1. Create a directory for the module files and enter it:

    ```
    $ mkdir ergaster
    $ cd ergaster
    ```

 2. Download the module tarball using `wget` utility:

    ```
    $ wget -O generatepass.tar.gz https://github.com/rvasilevsk/ergaster/tarball/master
    ```

    Alternatively, you can use the `curl` tool to download the module tarball:

    ```
    $ curl -L -o generatepass.tar.gz https://github.com/rvasilevsk/ergaster/tarball/master
    ```

 3. Extract the tarball and install the module:

    ```
    $ tar -xzf ergaster.tar.gz --strip=1
    $ python setup.py install
    ```
## Usage Examples

Arithmetic with complex numbers (imaginary part is zero):

```python
>>> 2+2
4
>>> 3+3
6
```

One-dimensional vectors subtraction:
```python
>>> 3-1
2
>>> 5-2
3
```

## Module Contents

## License

Licensed under the [MIT License]().

## Author

Roman Vasilevskiy (roman.vasilevsk@example.com) (gmail)