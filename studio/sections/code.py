"""An editor window that types the same feature in SQL, Java, Python and TypeScript."""

from __future__ import annotations

import re

from ..content import SNIPPETS
from ..svg import MARGIN, WIDTH, Doc
from ..theme import Theme
from ..typography import face

PANE_SECONDS = 9
TYPE_FROM, TYPE_TO = 0.3, 6.4  # seconds into a pane during which lines are typed
SIZE = 13.5
LINE = 21
TOP = 64
TAB_H = 42
CODE_Y = TOP + TAB_H + 28
GUTTER = 46
HEIGHT = CODE_Y + 17 * LINE + 34

KEYWORDS = {
    "sql": "WITH AS SELECT FROM GROUP BY LEFT JOIN ON WHERE BETWEEN AND ORDER OVER NULLS FIRST",
    "java": "public class private final return int new",
    "python": "from import class def return",
    "typescript": "export function const new return if as",
}
_TOKEN = re.compile(
    r"""
    (?P<comment>--.*$|//.*$|\#.*$)
    |(?P<string>\"\"\".*?\"\"\"|"[^"]*"|'[^']*'|`[^`]*`)
    |(?P<annotation>@\w+)
    |(?P<number>\b\d+(?:\.\d+)?\b)
    |(?P<word>\b[A-Za-z_]\w*\b)
    """,
    re.VERBOSE,
)


def tokenize(line: str, language: str) -> list[tuple[int, str, str]]:
    """Split a line into (column, text, class) tokens for highlighting."""
    keywords = set(KEYWORDS[language].split())
    tokens = []
    for match in _TOKEN.finditer(line):
        kind, text = match.lastgroup, match.group()
        if kind == "word":
            if text in keywords:
                kind = "keyword"
            elif text[0].isupper() and not text.isupper():
                kind = "type"
            elif line[match.end() : match.end() + 1] == "(":
                kind = "call"
            else:
                continue
        tokens.append((match.start(), text, kind))
    return tokens


def _render_line(doc: Doc, line: str, language: str, x: float, y: float, advance: float) -> str:
    """Base ink for the whole line, with highlighted tokens drawn over blanked columns."""
    tokens = tokenize(line, language)
    plain = list(line)
    for col, text, _ in tokens:
        plain[col : col + len(text)] = " " * len(text)
    parts = []
    base = "".join(plain).rstrip()
    if base:
        parts.append(doc.text(x, y, base, "mono", 400, SIZE, "cplain"))
    for col, text, kind in tokens:
        parts.append(doc.text(x + col * advance, y, text, "mono", 400, SIZE, f"c{kind}"))
    return "".join(parts)


def render(theme: Theme) -> str:
    languages = ", ".join(lang for _, lang, _ in SNIPPETS)
    doc = Doc(theme, f"Code window cycling through one feature written in {languages}", HEIGHT)
    t = theme
    mono = face("mono", 400)
    advance = mono.width("M", SIZE)
    loop = PANE_SECONDS * len(SNIPPETS)
    slice_pct = 100 / len(SNIPPETS)
    panel_x, panel_w = MARGIN, WIDTH - 2 * MARGIN
    code_x = panel_x + GUTTER

    doc.define(
        f'<clipPath id="editor"><rect x="{panel_x}" y="{TOP}" width="{panel_w}" '
        f'height="{HEIGHT - TOP}" rx="14"/></clipPath>'
    )
    doc.style(
        f".cplain{{fill:{t.ink}}}.ckeyword{{fill:{t.keyword}}}.cstring{{fill:{t.string}}}"
        f".ctype{{fill:{t.type}}}.cnumber{{fill:{t.number}}}.ccomment{{fill:{t.comment}}}"
        f".cannotation{{fill:{t.type}}}.ccall{{fill:{t.mint}}}"
        f".pane,.tabon{{opacity:0;animation:pane {loop}s linear infinite}}"
        f"@keyframes pane{{0%{{opacity:0}}.8%,{slice_pct - 1:.2f}%{{opacity:1}}"
        f"{slice_pct:.2f}%,100%{{opacity:0}}}}"
        f".cov,.caret{{animation-duration:{loop}s;"
        "animation-iteration-count:infinite;animation-timing-function:linear}",
        ".pane,.tabon{animation:none;opacity:0}.p0{opacity:1}.cov,.caret{display:none}",
    )

    doc.add(
        doc.section_header("02", "ONE FEATURE, FOUR LANGUAGES", "SQL  ·  JAVA  ·  PYTHON  ·  TS")
    )
    doc.add(
        f'<rect class="card" x="{panel_x}" y="{TOP}" width="{panel_w}" height="{HEIGHT - TOP}" '
        'rx="14"/>',
        f'<line class="rule" x1="{panel_x}" y1="{TOP + TAB_H}" x2="{panel_x + panel_w}" '
        f'y2="{TOP + TAB_H}"/>',
    )

    # Tabs: a muted base layer with an active layer that fades in on its turn.
    tab_x = panel_x + 18
    tab_face = face("mono", 500)
    for i, (filename, _, _) in enumerate(SNIPPETS):
        width = tab_face.width(filename, 12) + 28
        delay = i * PANE_SECONDS
        text_y = TOP + 26
        doc.add(
            doc.text(tab_x + 14, text_y, filename, "mono", 500, 12, "faint"),
            f'<g class="tabon p{i}" style="animation-delay:{delay}s">'
            f'<rect x="{tab_x}" y="{TOP + 8}" width="{width:.1f}" height="{TAB_H - 16}" rx="7" '
            f'fill="{t.accent}" fill-opacity=".14"/>'
            f"{doc.text(tab_x + 14, text_y, filename, 'mono', 500, 12, 'ink')}</g>",
        )
        doc.add(
            f'<g class="tabon p{i}" style="animation-delay:{delay}s">'
            f'<rect x="{tab_x}" y="{TOP + TAB_H - 1.5}" width="{width:.1f}" '
            f'height="2" fill="{t.mint}"/></g>'
        )
        tab_x += width + 6

    doc.add('<g clip-path="url(#editor)">')
    for pane, (_, language, source) in enumerate(SNIPPETS):
        lines = source.split("\n")
        delay = pane * PANE_SECONDS
        total_chars = sum(max(len(line), 1) for line in lines)
        elapsed = TYPE_FROM
        rendered, covers, caret_frames = [], [], ["0%{opacity:1}"]
        for n, line in enumerate(lines):
            y = CODE_Y + n * LINE
            rendered.append(doc.text(code_x - 14, y, str(n + 1), "mono", 400, 11.5, "faint", "end"))
            if not line:
                continue
            rendered.append(_render_line(doc, line, language, code_x, y, advance))

            duration = (TYPE_TO - TYPE_FROM) * max(len(line), 1) / total_chars
            start = elapsed / loop * 100
            end = (elapsed + duration) / loop * 100
            elapsed += duration
            width = len(line) * advance
            name = f"c{pane}l{n}"
            doc.style(
                f"@keyframes {name}{{0%,{start:.2f}%{{transform:translateX(0)}}"
                f"{end:.2f}%,100%{{transform:translateX({width:.1f}px)}}}}"
                f".{name}{{animation-name:{name};animation-timing-function:steps({len(line)})}}"
            )
            covers.append(
                f'<rect class="cov {name}" x="{code_x - 1}" y="{y - LINE + 6}" '
                f'width="{panel_w}" height="{LINE}" fill="{t.panel}"/>'
            )
            at = f"translate({width:.1f}px,{n * LINE}px)"
            caret_frames.append(
                f"{start:.2f}%{{transform:translate(0,{n * LINE}px)}}{end:.2f}%{{transform:{at}}}"
            )

        caret_name = f"caret{pane}"
        last = caret_frames[-1].split("{transform:")[-1].rstrip("}")
        doc.style(
            f"@keyframes {caret_name}{{{''.join(caret_frames[1:])}100%{{transform:{last}}}}}"
            f".{caret_name}{{animation-name:{caret_name}}}"
        )
        doc.add(
            f'<g class="pane p{pane}" style="animation-delay:{delay}s">',
            *rendered,
            *[
                c.replace('class="cov', f'style="animation-delay:{delay}s" class="cov')
                for c in covers
            ],
            f'<rect class="caret {caret_name}" style="animation-delay:{delay}s" x="{code_x}" '
            f'y="{CODE_Y - LINE + 7}" width="2" height="{LINE - 3}" fill="{t.accent}"/>',
            "</g>",
        )
    doc.add("</g>")

    doc.add(
        doc.label_text(
            panel_x + panel_w - 18, HEIGHT - 14, "REFERENCE SNIPPETS", "faint", "end", 10, 1.6
        ),
    )
    return doc.render()
