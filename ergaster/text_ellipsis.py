def render_lines(lines_count):
    s = "abcdefghijklmnopqrstuvwxyz"
    yield from ("%d: %s" % (i + 1, s) for i in range(lines_count))


def render_text(lines_count):
    return "\n".join(render_lines(lines_count))


#######################################################################################################################
def lines_width_height(lines):
    w, h = 0, 0
    for ln in lines:
        w = max(w, len(ln))
        h += 1
    return w, h


def text_width_height(text):
    return lines_width_height(text.splitlines(False))


#######################################################################################################################
def ellipsis_line(s, width, ellipsis_str="..."):
    l = len(s)
    if l <= width:
        return s
    ll = len(ellipsis_str)
    lll = width - ll
    if lll <= 0:
        return s[:width]
    return s[:lll] + ellipsis_str


#######################################################################################################################
def el_text_middle_str(width, lines_count, middle_ellipsis_str="..."):
    s = "%s (%d lines)" % (middle_ellipsis_str, lines_count)
    if len(s) <= width:
        return s
    s = "%s (%d)" % (middle_ellipsis_str, lines_count)
    if len(s) <= width:
        return s
    s = "%s" % middle_ellipsis_str
    if len(s) <= width:
        return s
    return s[:width]


def el_text_lines_1(height, lines):
    if height < 0:
        raise ValueError("height < 0")
    if height <= 1:
        yield from lines[:height]
    elif height == 2:
        yield from lines[:1]
    else:
        yield from lines[: height - 2]


def el_text_lines(
    width,
    height,
    lines_count,
    lines,
    last_line,
    ellipsis_str="...",
    middle_ellipsis_str="...",
):
    if lines_count <= height:
        yield from (ellipsis_line(ln, width, ellipsis_str) for ln in lines[:height])
        return
    yield from (
        ellipsis_line(ln, width, ellipsis_str) for ln in el_text_lines_1(height, lines)
    )
    if height > 1:
        yield el_text_middle_str(width, lines_count, middle_ellipsis_str)
    if height > 2:
        yield ellipsis_line(last_line, width, ellipsis_str)


#######################################################################################################################
class TextEllipsis:
    def __init__(
        self,
        width,
        height,
        line_seq=(),
        text=None,
        ellipsis_str="...",
        middle_ellipsis_str="...",
    ):
        assert width >= 0
        assert height >= 0
        self.ellipsis_str = ellipsis_str
        self.middle_ellipsis_str = middle_ellipsis_str
        self.width = width
        self.height = height
        self.lines_count = 0
        self.lines = []
        self.last_line = None
        if line_seq:
            self.feed_line_seq(line_seq)
        if text is not None:
            self.feed_text(text)

    def feed_line(self, line):
        if len(self.lines) < self.height:
            self.lines.append(line)
        self.lines_count += 1
        self.last_line = line

    def feed_line_seq(self, seq):
        for line in seq:
            self.feed_line(line)

    def feed_text(self, text):
        lines = text.splitlines(False)
        self.feed_line_seq(lines)

    def as_lines(self):
        yield from el_text_lines(
            self.width,
            self.height,
            self.lines_count,
            self.lines,
            self.last_line,
            self.ellipsis_str,
            self.middle_ellipsis_str,
        )

    def as_text(self):
        return "\n".join(self.as_lines())


#######################################################################################################################
def text_ellipsis(
    text, width=80, height=10, ellipsis_str="...", middle_ellipsis_str="..."
):
    obj = TextEllipsis(
        width,
        height,
        text=text,
        ellipsis_str=ellipsis_str,
        middle_ellipsis_str=middle_ellipsis_str,
    )
    return obj.as_text()
