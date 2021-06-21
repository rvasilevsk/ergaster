import os
import sys
from zipfile import ZipFile


#######################################################################################################################
def is_valid_relative_path(path):
    if not path:
        return False
    if path[0] in ("/", "\\", "~"):
        return False
    if ":" in path:  # c: (windows)
        return False
    return True


#######################################################################################################################
def make_dirs(path):
    if not os.path.exists(path):
        os.makedirs(path)
        return True
    if not os.path.isdir(path):
        raise FileExistsError("path exists but not a dir: " + str(path))
    return False


def make_dirs_by_filename(filename):
    path = os.path.dirname(filename)
    return make_dirs(path)


#######################################################################################################################
def open_read_utf8(filename):
    return open(str(filename), "r", encoding="utf8")


def open_write_utf8(filename):
    return open(str(filename), "wt", encoding="utf8")


def open_read_binary(filename):
    return open(str(filename), "rb")


def open_write_binary(filename):
    return open(str(filename), "wb")


#######################################################################################################################
def file_read_utf8(filename):
    return open_read_utf8(filename).read()


def file_write_utf8(filename, content):
    open_write_utf8(filename).write(content)


def file_read_binary(filename):
    return open_read_binary(filename).read()


def file_write_binary(filename, content):
    open_write_binary(filename).write(content)


#######################################################################################################################
def md_syntax_by_filename(filename):
    filename = filename.lower()
    if filename.endswith(
        (
            ".py",
            ".py3",
            ".pyw",
        )
    ):
        return "python"
    if filename.endswith(
        (
            ".php",
            ".htm",
            ".html",
        )
    ):
        return "html"
    if filename.endswith(
        (
            ".sh",
            ".bash",
        )
    ):
        return "bash"
    if filename.endswith(
        (
            ".bat",
            ".cmd",
        )
    ):
        return "bat"
    return ""


#######################################################################################################################
def ell_text(text, width=80, height=10):
    import text_ellipsis

    return text_ellipsis.text_ellipsis(text, width, height)


def is_binary(s):
    return isinstance(s, bytes)


def write_filename_n_content_txt(out, filename, content, width, height):
    if is_binary(content):
        res = "BINARY"
    else:
        res = ell_text(content, width, height)
    seq = ("--- ", filename, " ---\n", res, "\n\n")
    for s in seq:
        out.write(s)


def write_filename_n_content_markdown(out, filename, content):
    qqq = "`" * 3
    syntax = md_syntax_by_filename(filename)
    if is_binary(content):
        content = "BINARY"
        syntax = ""
    seq = ("### ", filename, "\n", qqq, syntax, "\n", content, "\n", qqq, "\n\n\n")
    for s in seq:
        out.write(s)


#######################################################################################################################
class FileWriterTxt:
    def __init__(self, out=None, width=80, height=10):
        self.out = sys.stdout if out is None else out
        self.width = width
        self.height = height

    def write_file(self, filename, content):
        assert is_valid_relative_path(filename)
        write_filename_n_content_txt(
            self.out, filename, content, self.width, self.height
        )

    def close(self):
        pass


class FileWriterMarkdown:
    def __init__(self, out=None):
        self.out = sys.stdout if out is None else out

    def write_file(self, filename, content):
        assert is_valid_relative_path(filename)
        write_filename_n_content_markdown(self.out, filename, content)

    def close(self):
        pass


class FileWriterMemory:
    def __init__(self, root):
        self.root = root
        self.filename_list = []
        self.content_dict = {}

    def write_file(self, filename, content):
        assert is_valid_relative_path(filename)
        self.filename_list.append(filename)
        self.content_dict[filename] = content

    def get_filenames(self):
        for filename in self.filename_list:
            yield os.path.join(self.root, filename)

    def close(self):
        pass


class FileWriterFs:
    def __init__(self, root, print_flag=False):
        self.root = root
        self.print_flag = print_flag

    def prnt(self, *args):
        if self.print_flag:
            print(*args)

    def write_file(self, filename, content):
        assert is_valid_relative_path(filename)
        filename = os.path.join(self.root, filename)
        filename = os.path.expanduser(filename)
        res = make_dirs_by_filename(filename)
        if res:
            self.prnt("make dir: ", os.path.dirname(filename))
        if is_binary(content):
            n = len(content)
            self.prnt("write binary (%d bytes) %s" % (n, filename))
            file_write_binary(filename, content)
        else:
            n = len(content)
            self.prnt("write text (%d chars) %s" % (n, filename))
            file_write_utf8(filename, content)

    def close(self):
        pass


class FileWriterZip:
    def __init__(self, zip_filename):
        self.filename = zip_filename
        path = os.path.expanduser(zip_filename)
        self.zip_file = ZipFile(path, "w")

    def write_file(self, filename, content):
        assert is_valid_relative_path(filename)
        self.zip_file.writestr(filename, content)

    def close(self):
        self.zip_file.close()


#######################################################################################################################
def example_filename_content_generator():
    content_bin = b"\x00\x00\x00\x00\x00\x00\x00\x00"
    content_py = """def fn(x):\n    return x**3"""
    content_php = """function fn(x) {\n    return x*x*x;\n}"""
    yield "file.bin.php", content_bin
    yield "file.py", content_py
    yield "file.php", content_php
    yield "dir/file2.py", content_py
    yield "dir/file2.php", content_php
    yield "dir2/dir3/dir4/file3.py", content_py
    yield "dir2/dir3/dir4/file3.php", content_php
    d, name = os.path.split(__file__)
    content = file_read_utf8(__file__)
    yield name, content


def example_x(vfs):
    for filename, content in example_filename_content_generator():
        vfs.write_file(filename, content)
    vfs.close()


def example_out():
    f = open_write_utf8("result.txt")
    vfs = FileWriterTxt(f)
    example_x(vfs)


def example_md():
    f = open_write_utf8("result.md")
    vfs = FileWriterMarkdown(f)
    example_x(vfs)


def example_fs(root="./result"):
    vfs = FileWriterFs(root)
    example_x(vfs)


def example_zip(zip_filename="result.zip"):
    vfs = FileWriterZip(zip_filename)
    example_x(vfs)


#######################################################################################################################
if __name__ == "__main__":
    example_out()
    example_md()
    example_fs()
    example_zip()
