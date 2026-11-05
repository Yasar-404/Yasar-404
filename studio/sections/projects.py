"""One linked card per project, each with a small looping scene of what the project does."""

from __future__ import annotations

from ..content import Project
from ..svg import EASE, MARGIN, WIDTH, Doc
from ..theme import Theme

HEIGHT = 186
LOOP = 8
SCENE_X, SCENE_Y, SCENE_W, SCENE_H = 640, 24, 248, 138


def _liftiq(doc: Doc) -> str:
    t = doc.theme
    bars = "".join(
        f'<rect class="bar" style="animation-delay:{i * 0.12:.2f}s" x="{22 + i * 34}" '
        f'y="{112 - h}" width="20" height="{h}" rx="4" fill="{t.accent}"/>'
        for i, h in enumerate((30, 46, 38, 60, 54, 74))
    )
    doc.style(
        f".bar{{transform-box:fill-box;transform-origin:bottom;animation:bar {LOOP}s {EASE} infinite}}"
        "@keyframes bar{0%{transform:scaleY(0)}12%,88%{transform:scaleY(1)}100%{transform:scaleY(0)}}",
        ".bar{animation:none}",
    )
    return (
        doc.label_text(22, 24, "ACTIVE MEMBERS", "faint", size=9.5, track=1.6)
        + f'<line x1="22" y1="112" x2="226" y2="112" stroke="{t.stroke}"/>{bars}'
    )


def _envguard(doc: Doc) -> str:
    t = doc.theme
    lines = (
        ("$ envguard scan ./project", "muted", 0.2),
        ("1 HIGH  1 MEDIUM  0 LOW", "ink", 1.4),
        ("AWS Access Key", "accent", 2.0),
        ("Value: AKIA************", "mintf", 2.6),
        ("exit 1", "faint", 3.2),
    )
    rows = "".join(
        f'<g class="term" style="animation-delay:{d}s">'
        f"{doc.text(16, 28 + i * 22, text, 'mono', 400, 11.5, cls)}</g>"
        for i, (text, cls, d) in enumerate(lines)
    )
    doc.style(
        f".term{{animation:term {LOOP}s linear infinite}}"
        "@keyframes term{0%{opacity:0}2%,84%{opacity:1}88%,100%{opacity:0}}"
        f".sweep{{animation:sweep {LOOP}s {EASE} infinite}}"
        "@keyframes sweep{0%{transform:translateY(0);opacity:.8}45%{transform:translateY(126px);"
        "opacity:.8}50%,100%{transform:translateY(126px);opacity:0}}",
        ".term{animation:none}.sweep{animation:none;opacity:0}",
    )
    return (
        rows + f'<rect class="sweep" x="0" y="6" width="{SCENE_W}" height="1.5" fill="{t.mint}"/>'
    )


def _shortener(doc: Doc) -> str:
    t = doc.theme
    doc.style(
        f".long{{animation:long {LOOP}s {EASE} infinite}}"
        "@keyframes long{0%,18%{opacity:1}34%,100%{opacity:0}}"
        f".pipe{{transform-box:fill-box;transform-origin:left;animation:pipe {LOOP}s {EASE} infinite}}"
        "@keyframes pipe{0%,18%{transform:scaleX(1)}36%,92%{transform:scaleX(.42)}"
        "100%{transform:scaleX(1)}}"
        f".short{{animation:short {LOOP}s {EASE} infinite}}"
        "@keyframes short{0%,30%{opacity:0}40%,90%{opacity:1}96%,100%{opacity:0}}",
        ".long,.pipe{animation:none}.long{opacity:0}.pipe{transform:scaleX(.42)}.short{animation:none}",
    )
    return (
        doc.label_text(16, 28, "POST /shorten", "muted", size=10.5, track=1.2)
        + f'<rect class="pipe" x="16" y="42" width="216" height="26" rx="6" fill="{t.accent}" '
        'fill-opacity=".2"/>'
        + f'<g class="long">{doc.text(24, 59, "example.com/a/very/long/path?q=1", "mono", 400, 10.5, "ink")}</g>'
        + f'<g class="short">{doc.text(24, 59, "/aZ3xK9q", "mono", 500, 11.5, "ink")}'
        + doc.label_text(16, 98, "GET /aZ3xK9q", "muted", size=10.5, track=1.2)
        + doc.text(16, 120, "302", "mono", 700, 15, "mintf")
        + doc.text(52, 120, "redirect", "sans", 400, 12.5, "muted")
        + "</g>"
    )


def _walkin(doc: Doc) -> str:
    t = doc.theme
    length = 3.1416 * 44
    doc.style(
        f".gauge{{stroke-dasharray:{length:.1f};animation:gauge {LOOP}s {EASE} infinite}}"
        f"@keyframes gauge{{0%{{stroke-dashoffset:{length:.1f}}}"
        f"22%,88%{{stroke-dashoffset:{length * 0.42:.1f}}}100%{{stroke-dashoffset:{length:.1f}}}}}"
        f".rw{{animation:rw {LOOP}s linear infinite}}"
        "@keyframes rw{0%{opacity:0}3%,72%{opacity:1}78%,100%{opacity:0}}",
        f".gauge{{animation:none;stroke-dashoffset:{length * 0.42:.1f}}}.rw{{animation:none}}",
    )
    rows = "".join(
        f'<g class="rw" style="animation-delay:{0.6 + i * 0.5}s">'
        f"{doc.label_text(132, 48 + i * 28, name, 'muted', size=10.5, track=1.4)}"
        f'<rect x="132" y="{54 + i * 28}" width="{w}" height="4" rx="2" fill="{c}"/></g>'
        for i, (name, w, c) in enumerate(
            (("BMI", 56, t.accent), ("BMR", 84, t.iris), ("TDEE", 72, t.mint))
        )
    )
    return (
        f'<path d="M22 96 a44 44 0 0 1 88 0" stroke="{t.stroke}" stroke-width="8" '
        'stroke-linecap="round"/>'
        f'<path class="gauge" d="M22 96 a44 44 0 0 1 88 0" stroke="{t.accent}" stroke-width="8" '
        'stroke-linecap="round"/>' + rows
    )


SCENES = {"liftiq": _liftiq, "envguard": _envguard, "shortener": _shortener, "walkin": _walkin}


def render(theme: Theme, project: Project) -> str:
    summary = " ".join(project.summary)
    doc = Doc(theme, f"{project.title}: {summary}", HEIGHT)
    t = theme
    left = MARGIN + 24
    doc.define(
        f'<clipPath id="scene"><rect width="{SCENE_W}" height="{SCENE_H}" rx="10"/></clipPath>'
    )
    doc.add(
        f'<rect class="card" x="{MARGIN}" y="6" width="{WIDTH - 2 * MARGIN}" '
        f'height="{HEIGHT - 12}" rx="14"/>',
        doc.label_text(left, 44, project.kind, "accent", size=10.5, track=2),
        doc.text(left, 80, project.title, "sans", 600, 27, "ink", track=-0.3),
        doc.text(left, 108, project.summary[0], "sans", 400, 14, "muted"),
        doc.text(left, 129, project.summary[1], "sans", 400, 14, "muted"),
    )
    x = left
    for tag in project.tags:
        doc.add(doc.label_text(x, 158, tag, "faint", size=10, track=1.3))
        x += len(tag) * 7.3 + 20
    doc.add(
        f'<g transform="translate({SCENE_X} {SCENE_Y})" clip-path="url(#scene)">'
        f'<rect width="{SCENE_W}" height="{SCENE_H}" rx="10" fill="{t.bg}"/>',
        SCENES[project.slug](doc),
        "</g>",
        f'<rect x="{SCENE_X}" y="{SCENE_Y}" width="{SCENE_W}" height="{SCENE_H}" rx="10" '
        f'stroke="{t.stroke}"/>',
    )
    return doc.render()
