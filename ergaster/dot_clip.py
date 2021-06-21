import os
import sys
from datetime import datetime

import pyperclip

from ergaster.file_writer import FileWriterFs, file_read_utf8
from ergaster.text_ellipsis import ellipsis_line


#######################################################################################################################
def is_windows():
    return os.name == "nt"


def chomp(x):
    if x.endswith("\r\n"):
        return x[:-2]
    if x.endswith("\n") or x.endswith("\r"):
        return x[:-1]
    return x


def cd_cwd_string():
    cwd = os.getcwd()
    if is_windows():
        return 'cd /d "%s"' % cwd
    else:
        return 'cd "%s"' % cwd


def real_path_string(path):
    # path = os.path.expanduser(path)
    path = os.path.abspath(path)
    path = auto_slashes(path)
    return path


def ddd():
    return datetime.today().strftime("%Y.%m.%d")


def mmm():
    return datetime.today().strftime("%Y.%m.%d %H:%M:%S")


#######################################################################################################################
def first_line_n_count(text):
    res = ""
    n = 0
    for ln in text.splitlines(False):
        if n == 0:
            res = ln
        n += 1
    return res, n


def shorten_to_line(text, width=40):
    ln, n = first_line_n_count(text)
    ln = ellipsis_line(ln, width)
    if n > 1:
        ln = "%s (lines: %d)" % (ln, n)
    return ln


#######################################################################################################################
def nix_slashes(path):
    return path.replace("\\", "/")


def win_slashes(path):
    return path.replace("/", "\\")


def auto_slashes(path):
    if is_windows():
        return win_slashes(path)
    else:
        return nix_slashes(path)


#######################################################################################################################
def name_content_py():
    self_root = os.path.dirname(__file__)
    py_files = "dot_clip.py text_ellipsis.py file_writer.py pyperclip/__init__.py pyperclip/__main__.py".split()
    for filename in py_files:
        src = os.path.join(self_root, filename)
        dst = os.path.join("dot_clip", filename)
        content = file_read_utf8(src)
        yield dst, content


#######################################################################################################################
def alias_cmd_seq():
    return (
        ("cv", "paste"),
        ("cc", "copy_args"),
        ("ccstdin", "copy_stdin"),
        ("ccd", "copy_cd"),
        ("crp", "copy_real_path"),
        ("cddd", "copy_ddd"),
        ("cmmm", "copy_mmm"),
    )


def commands_help_lines():
    yield "install_win"
    yield "install_nix"
    for _alias, inner_cmd in alias_cmd_seq():
        yield inner_cmd


def doskey_lines(install_dir):
    path = os.path.join(install_dir, "dot_clip/dot_clip.py")
    path = win_slashes(path)
    yield 'dot_clip=python3 "%s" $*' % path
    yield from (
        '%s=python3 "%s" %s $*' % (alias, path, inner_cmd)
        for (alias, inner_cmd) in alias_cmd_seq()
    )


def bat_name_content(install_dir):
    path = os.path.join(install_dir, "dot_clip/dot_clip.py")
    path = win_slashes(path)
    yield "dot_clip.cmd", "@python3 %s %%*" % path
    for alias, inner_cmd in alias_cmd_seq():
        # yield alias + '.cmd', '@dot_clip %s %%* ' % inner_cmd
        yield alias + ".cmd", '@python3 "%s" %s %%* ' % (path, inner_cmd)
    yield "dot_clip.doskey", "\n".join(doskey_lines(install_dir))


def nix_alias_body(install_dir):
    path = os.path.join(install_dir, "dot_clip/dot_clip.py")
    path = nix_slashes(path)
    yield "dot_clip", "python3 %s" % path
    for alias, inner_cmd in alias_cmd_seq():
        yield alias, "dot_clip %s" % inner_cmd


def nix_alias_lines(install_dir):
    return (
        "alias %s='%s'" % (alias, body) for (alias, body) in nix_alias_body(install_dir)
    )


def name_content_unix(install_dir):
    yield "dot_clip_aliases.sh", "\n".join(nix_alias_lines(install_dir))


#######################################################################################################################
class Installer:
    def __init__(self, writer):
        self.writer = writer

    def installation_root(self):
        root = getattr(self.writer, "root", "")
        root = os.path.abspath(root)
        return root

    def filename_content_seq_windows(self):
        yield from name_content_py()
        yield from bat_name_content(self.installation_root())

    def filename_content_seq_nix(self):
        yield from name_content_py()
        yield from name_content_unix(self.installation_root())

    def install_windows(self):
        writer = self.writer
        for filename, content in self.filename_content_seq_windows():
            writer.write_file(filename, content)

    def install_nix(self):
        writer = self.writer
        for filename, content in self.filename_content_seq_nix():
            writer.write_file(filename, content)


#######################################################################################################################
class RunInstallWin:
    def __init__(self, root):
        root = os.path.abspath(root)
        self.root = root
        self.writer = FileWriterFs(root, print_flag=True)
        self.inst = Installer(self.writer)

    def name_content_seq(self):
        return self.inst.filename_content_seq_windows()

    def run(self):
        name_content = self.name_content_seq()
        for filename, content in name_content:
            self.writer.write_file(filename, content)


class RunInstallNix(RunInstallWin):
    def name_content_seq(self):
        return self.inst.filename_content_seq_nix()


#######################################################################################################################
class RunUsage:
    def __init__(self, usage):
        self.out = sys.stdout
        self.usage = usage

    def run(self):
        self.out.write(self.usage)
        self.out.write("\n")


class RunPaste:
    def __init__(self):
        self.out = sys.stdout

    def run(self):
        text = pyperclip.paste()
        self.out.write(text)
        self.out.write("\n")


class RunCopy:
    def __init__(self, text):
        self.out = sys.stdout
        self.text = text

    def run(self):
        self.out.write("clipboard << ")
        ln = shorten_to_line(self.text)
        self.out.write(ln)
        self.out.write("\n")
        pyperclip.copy(self.text)


class RunCopyStdin:
    def __init__(self):
        self.stdin = sys.stdin

    def run(self):
        text = self.stdin.read()
        RunCopy(text).run()


#######################################################################################################################
def get_run(inner_cmd, args):
    if not inner_cmd:
        usage = ["Usage: dot_clip <command>"] + list(commands_help_lines())
        usage = "\n".join(usage)
        return RunUsage(usage)
    n = len(args)

    if inner_cmd == "install_win":
        if n == 0:
            return RunUsage("install_win: no arguments")
        return RunInstallWin(args[0])
    if inner_cmd == "install_nix":
        if n == 0:
            return RunUsage("install_nix: no arguments")
        return RunInstallNix(args[0])

    if inner_cmd == "paste":
        return RunPaste()
    if inner_cmd == "copy_args":
        if n == 0:
            return RunUsage("copy_args: no arguments")
        return RunCopy(" ".join(args))
    if inner_cmd == "copy_stdin":
        return RunCopyStdin()
    if inner_cmd == "copy_cd":
        return RunCopy(cd_cwd_string())
    if inner_cmd == "copy_real_path":
        if n == 0:
            return RunUsage("copy_real_path: no arguments")
        return RunCopy(real_path_string(args[0]))
    if inner_cmd == "copy_ddd":
        return RunCopy(ddd())
    if inner_cmd == "copy_mmm":
        return RunCopy(mmm())
    usage = "Unknown command %s" % inner_cmd
    return RunUsage(usage)


def do_run(inner_cmd, args):
    get_run(inner_cmd, args).run()


def main():
    args = sys.argv
    if len(args) < 2:
        do_run(None, ())
    else:
        do_run(args[1], args[2:])


if __name__ == "__main__":
    main()
    # do_run(None, ())

    # do_run('install_win', ())
    # do_run('install_nix', ())
    #
    # do_run('install_win', ('result_win',))
    # do_run('install_nix', ('result_nix',))

    # do_run('paste', ())
    # do_run('copy_args', ('123', '456\n\n\n\n'))
    # # do_run('copy_stdin', ())
    # do_run('copy_cd', ())
    # do_run('copy_real_path', ('.'))
    # do_run('copy_ddd', ())
    # do_run('copy_mmm', ())
