import pytest

from ergaster.dot_clip import first_line_n_count, get_run, shorten_to_line

data = (
    ("", "", 0),
    ("aaa", "aaa", 1),
    ("aaa\n\n\n", "aaa", 3),
)


@pytest.mark.parametrize("text, line, n", data)
def test_first_line_n_count(text, line, n):
    assert first_line_n_count(text) == (line, n)


data = (
    ("", ""),
    ("aaa", "aaa"),
    ("aaa\n\n\n", "aaa (lines: 3)"),
)


@pytest.mark.parametrize("text, result", data)
def test_shorten_to_line(text, result):
    assert shorten_to_line(text) == result


win_files = """
dot_clip/dot_clip_nt.py
dot_clip/text_ellipsis.py
dot_clip/file_writer.py
dot_clip/pyperclip/__init__.py
dot_clip/pyperclip/__main__.py'
""".split()


def test_get_run():
    assert get_run(None, ()).usage.startswith("Usage: dot_clip <command>")

    assert get_run("install_nix", ()).usage.startswith("install_nix: no arguments")
    assert get_run("install_nix", ("~/temp")).__class__.__name__ == "RunInstallNix"
    assert get_run("install_win", ()).usage.startswith("install_win: no arguments")
    assert get_run("install_win", ("c:/temp")).__class__.__name__ == "RunInstallWin"

    assert get_run("paste", ()).__class__.__name__ == "RunPaste"

    assert get_run("copy_args", ()).usage.startswith("copy_args: no arguments")
    assert get_run("copy_args", ("abc",)).text == "abc"
    assert (
        get_run(
            "copy_args",
            (
                "abc",
                "def",
            ),
        ).text
        == "abc def"
    )

    assert get_run("copy_stdin", ()).__class__.__name__ == "RunCopyStdin"

    assert get_run("copy_cd", ()).text.startswith("cd ")

    assert get_run("copy_real_path", ()).usage.startswith(
        "copy_real_path: no arguments"
    )
    # assert get_run("copy_real_path", ("test_dot_clip.py",)).text == __file__

    assert get_run("copy_ddd", (".",)).text
    assert get_run("copy_mmm", (".",)).text

    assert get_run("unknown_cmd", (".",)).usage.startswith(
        "Unknown command unknown_cmd"
    )


# def test_windows_install():
#     root = 'c:/bin/bin_python'
#     root = 'result'
#     writer = FileWriterFs(root)
#     inst = Installer(writer)
#     inst.install_windows()
#
#     # root = '~/dot_python'
#     # writer = FileWriterFs(root)
#     # inst = Installer(writer)
#     # inst.install_nix()
#
#     f = open_write_utf8('result.win.md')
#     writer = FileWriterMarkdown(f)
#     inst = Installer(writer)
#     inst.install_windows()
#
#     f = open_write_utf8('result.nix.md')
#     writer = FileWriterMarkdown(f)
#     inst = Installer(writer)
#     inst.install_nix()
