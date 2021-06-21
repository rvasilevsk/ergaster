import pytest

from ergaster.file_writer import (
    file_read_binary,
    file_read_utf8,
    file_write_binary,
    file_write_utf8,
    is_valid_relative_path,
    md_syntax_by_filename,
)


#######################################################################################################################
@pytest.fixture(scope="module")
def utf8_text():
    return "Привет мир\n" * 10


@pytest.fixture(scope="module")
def binary_data():
    return b"\x00\xC2\xA9\x20\xF0\x9D\x8C\x86\x20\xE2\x98\x83"
    # data = (chr(i) for i in range(256))
    # data = b''.join(data)
    # return data


#######################################################################################################################
data = ("aaa/bbb",)


@pytest.mark.parametrize("path", data)
def test_is_valid_relative_path(path):
    assert is_valid_relative_path(path)


data = (
    "",
    "~",
    "/",
    "\\",
    "c:/",
    "c:\\",
    "d:aaa/bbb",
)


@pytest.mark.parametrize("path", data)
def test_not_is_valid_relative_path(path):
    assert is_valid_relative_path(path) is False


#######################################################################################################################
def test_file_read_write_utf8(tmp_path, utf8_text):
    file_name = tmp_path / "utf8.txt"
    file_write_utf8(file_name, utf8_text)
    assert file_read_utf8(file_name) == utf8_text


def test_file_read_write_utf8_raises(tmp_path, binary_data):
    file_name = tmp_path / "utf8.txt"
    with pytest.raises(TypeError):
        file_write_utf8(file_name, binary_data)


def test_file_read_write_binary(tmp_path, binary_data):
    file_name = tmp_path / "binary_file"
    file_write_binary(file_name, binary_data)
    assert file_read_binary(file_name) == binary_data


def test_file_read_write_binary_raises(tmp_path, utf8_text):
    file_name = tmp_path / "binary_file"
    with pytest.raises(TypeError):
        file_write_binary(file_name, utf8_text)
        file_write_binary(file_name, utf8_text)


#######################################################################################################################
data = (
    ("", ""),
    ("file", ""),
    ("file.exe", ""),
    ("file.py", "python"),
    ("file.Py", "python"),
    ("file.PY", "python"),
    ("file.py3", "python"),
    ("file.pyw", "python"),
    ("file.php", "html"),
    ("file.htm", "html"),
    ("file.html", "html"),
    ("file.sh", "bash"),
    ("file.bash", "bash"),
)


@pytest.mark.parametrize("filename, result", data)
def test_text_width_height(filename, result):
    assert md_syntax_by_filename(filename) == result
