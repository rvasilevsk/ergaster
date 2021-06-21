import pytest

from ergaster.text_ellipsis import (
    TextEllipsis,
    el_text_lines,
    el_text_lines_1,
    el_text_middle_str,
    ellipsis_line,
    render_lines,
    render_text,
    text_ellipsis,
    text_width_height,
)

#######################################################################################################################
data = (
    (0, ""),
    (1, "1: abcdefghijklmnopqrstuvwxyz"),
    (2, "1: abcdefghijklmnopqrstuvwxyz\n2: abcdefghijklmnopqrstuvwxyz"),
)


@pytest.mark.parametrize("line_count, result", data)
def test_render_text(line_count, result):
    assert render_text(line_count) == result


#######################################################################################################################
data = (
    ("", 0, 0),
    ("\n", 0, 1),
    ("\n\n", 0, 2),
    ("a", 1, 1),
    ("a\n", 1, 1),
    ("a\n\n", 1, 2),
    ("aaa", 3, 1),
    ("aa\n", 2, 1),
    ("aaaa\naa\n", 4, 2),
)


@pytest.mark.parametrize("text, width, height", data)
def test_text_width_height(text, width, height):
    assert text_width_height(text) == (width, height)


#######################################################################################################################
data = (
    ("", 5, ""),
    ("abcd", 5, "abcd"),
    ("abcde", 5, "abcde"),
    ("abcdef", 5, "ab..."),
    ("abcdef", 0, ""),
    ("abcdef", 1, "a"),
    ("abcdef", 2, "ab"),
    ("abcdef", 3, "abc"),
    ("abcdef", 4, "a..."),
)


@pytest.mark.parametrize("s, w, result", data)
def test_el(s, w, result):
    assert ellipsis_line(s, w) == result


#######################################################################################################################
data = (
    (0, 100, ". . .", ""),
    (1, 100, ". . .", "."),
    (2, 100, ". . .", ". "),
    (3, 100, ". . .", ". ."),
    (7, 100, ". . .", ". . ."),
    (11, 100, ". . .", ". . . (100)"),
    (16, 100, ". . .", ". . . (100)"),
    (17, 100, ". . .", ". . . (100 lines)"),
    (30, 100, ". . .", ". . . (100 lines)"),
)


@pytest.mark.parametrize("w, lines_count, el, result", data)
def test_el_text_middle_str(w, lines_count, el, result):
    assert el_text_middle_str(w, lines_count, el) == result


lines_5 = "a b c d e".split()
data = (
    (0, lines_5, ""),
    (1, lines_5, "a"),
    (2, lines_5, "a"),
    (3, lines_5, "a"),
    (4, lines_5, "a\nb"),
)


@pytest.mark.parametrize("height, lines, result", data)
def test_el_text_lines_1(height, lines, result):
    res = el_text_lines_1(height, lines)
    res = "\n".join(res)
    assert res == result


data = (
    (50, 0, lines_5, ""),
    (50, 1, lines_5, "a"),
    (50, 2, lines_5, "a\n... (5 lines)"),
    (50, 3, lines_5, "a\n... (5 lines)\ne"),
    (50, 4, lines_5, "a\nb\n... (5 lines)\ne"),
)


@pytest.mark.parametrize("width, height, lines, result", data)
def test_el_text_lines(width, height, lines, result):
    lines_count = len(lines)
    last_line = lines[-1]
    res = el_text_lines(width, height, lines_count, lines, last_line)
    res = "\n".join(res)
    assert res == result


lines_5 = "aaaa bbbb cccc dddd eeee".split()
data = (
    (3, 0, lines_5, ">", "..", ""),
    (3, 1, lines_5, ">", "..", "aa>"),
    (3, 2, lines_5, ">", "..", "aa>\n.."),
    (3, 3, lines_5, ">", "..", "aa>\n..\nee>"),
    (3, 4, lines_5, ">", "..", "aa>\nbb>\n..\nee>"),
    (5, 4, lines_5, ">", "..", "aaaa\nbbbb\n..\neeee"),
    (6, 4, lines_5, ">", "..", "aaaa\nbbbb\n.. (5)\neeee"),
    (30, 4, lines_5, ">", "..", "aaaa\nbbbb\n.. (5 lines)\neeee"),
)


@pytest.mark.parametrize(
    "width, height, lines, ellipsis_str, middle_ellipsis_str, result", data
)
def test_el_text_lines_ellipsis_str(
    width, height, lines, ellipsis_str, middle_ellipsis_str, result
):
    lines_count = len(lines)
    last_line = lines[-1]
    res = el_text_lines(
        width, height, lines_count, lines, last_line, ellipsis_str, middle_ellipsis_str
    )
    res = "\n".join(res)
    assert res == result


#######################################################################################################################
lines_99 = list(render_lines(99))
text_99 = render_text(99)

data = (
    (TextEllipsis(3, 0, line_seq=lines_99), ""),
    (TextEllipsis(3, 0, text=text_99), ""),
    (TextEllipsis(0, 3, line_seq=lines_99), "\n\n"),
    (TextEllipsis(0, 3, text=text_99), "\n\n"),
    (TextEllipsis(1, 3, line_seq=lines_99), "1\n.\n9"),
    (TextEllipsis(1, 3, text=text_99), "1\n.\n9"),
    (TextEllipsis(5, 3, line_seq=lines_99), "1:...\n...\n99..."),
    (TextEllipsis(5, 3, text=text_99), "1:...\n...\n99..."),
    (TextEllipsis(8, 4, line_seq=lines_99), "1: ab...\n2: ab...\n... (99)\n99: a..."),
    (TextEllipsis(8, 4, text=text_99), "1: ab...\n2: ab...\n... (99)\n99: a..."),
)


@pytest.mark.parametrize("cls, result", data)
def test_el_text_class(cls, result):
    assert cls.as_text() == result


def test_w_h_ranges():
    text = render_text(20)
    for h in range(1, 10):  # todo 0
        for w in range(1, 10):
            stripped = TextEllipsis(
                w, h, text=text, ellipsis_str=">>>", middle_ellipsis_str=". . ."
            ).as_text()
            assert text_width_height(stripped) == (w, h)


text = "aaa\nbbb\nccc\nddd"
data = (
    (text, 80, 10, text),
    (text, 2, 10, "aa\nbb\ncc\ndd"),
)


@pytest.mark.parametrize("text, width, height, result", data)
def test_last(text, width, height, result):
    assert text_ellipsis(text, width, height) == result
