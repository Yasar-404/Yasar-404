"""Hero: an outlined wordmark that draws itself above a cycling stack cross-section."""

from __future__ import annotations

from ..content import HEADLINE, LAYERS, STATUS, TAGLINE, WORDMARK
from ..svg import EASE, MARGIN, WIDTH, Doc, num
from ..theme import Theme
from ..typography import face

HEIGHT = 420
BASELINE = 198
RULE_Y = 222
CYCLE = 16  # seconds for one pass through all four layers


def _wordmark(doc: Doc, width: float) -> str:
    """Draw each glyph as its own path, so the letters can reveal in sequence."""
    f = face("display", 800)
    size = width / f.width(WORDMARK, 1, -0.015)
    scale = size / f.upm
    paths, clips, cursor = [], [], 0.0
    for i, char in enumerate(WORDMARK):
        glyph = f.glyph(char)
        d = f.path(glyph)
        if d:
            at = f"translate({num(MARGIN + cursor)} {BASELINE}) scale({scale:.5f} {-scale:.5f})"
            paths.append(
                f'<path class="wm" pathLength="1" style="animation-delay:{0.2 + i * 0.12:.2f}s" '
                f'transform="{at}" d="{d}"/>'
            )
            clips.append(f'<path transform="{at}" d="{d}"/>')
        cursor += (f.advances[glyph] - 0.015 * f.upm) * scale
    doc.define(f'<clipPath id="wclip">{"".join(clips)}</clipPath>')
    return "".join(paths)


def _layer_stack(doc: Doc) -> str:
    """Isometric cross-section of the stack; the active layer lights up with its label."""
    cx, half_w, half_h, step = 812, 78, 30, 30
    top = 272
    parts = []
    for i in range(len(LAYERS) - 1, -1, -1):
        cy = top + i * step
        points = f"{cx},{cy - half_h} {cx + half_w},{cy} {cx},{cy + half_h} {cx - half_w},{cy}"
        parts.append(f'<polygon class="lay" points="{points}"/>')
        parts.append(
            f'<polygon class="lit" points="{points}" style="animation-delay:{i * CYCLE / 4}s"/>'
        )
    return "".join(parts)


def _layer_copy(doc: Doc) -> str:
    parts = []
    for i, (name, tools) in enumerate(LAYERS):
        label = doc.label_text(MARGIN, 314, name, "accent", size=12, track=2.4)
        value = doc.text(MARGIN + 104, 314, tools, "sans", 400, 15, "muted")
        parts.append(
            f'<g class="ph ph{i}" style="animation-delay:{i * CYCLE / 4}s">{label}{value}</g>'
        )
    return "".join(parts)


def render(theme: Theme) -> str:
    doc = Doc(theme, "Yasar K, full-stack engineer and product designer, Chennai", HEIGHT)
    inner = WIDTH - 2 * MARGIN
    t = theme
    doc.define(
        f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse">'
        f'<circle cx="1" cy="1" r="1" fill="{t.dot}"/></pattern>'
        f'<radialGradient id="halo" cx=".5" cy=".4" r=".7">'
        f'<stop offset="0" stop-color="{t.accent}" stop-opacity=".22"/>'
        f'<stop offset=".5" stop-color="{t.iris}" stop-opacity=".07"/>'
        f'<stop offset="1" stop-color="{t.accent}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="aurora" gradientUnits="userSpaceOnUse" x1="{MARGIN}" y1="0" '
        f'x2="{WIDTH - MARGIN}" y2="0"><stop offset="0" stop-color="{t.accent}"/>'
        f'<stop offset=".5" stop-color="{t.iris}"/><stop offset="1" stop-color="{t.mint}"/>'
        f"</linearGradient>"
        f'<linearGradient id="sheen"><stop offset="0" stop-color="{t.gleam}" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="{t.gleam}" stop-opacity=".95"/>'
        f'<stop offset="1" stop-color="{t.gleam}" stop-opacity="0"/></linearGradient>'
        f'<clipPath id="frame"><rect width="{WIDTH}" height="{HEIGHT}" rx="16"/></clipPath>'
    )
    doc.style(
        f".wm{{fill:{t.ink};fill-opacity:0;stroke:{t.accent};stroke-width:14;"
        f"stroke-dasharray:1;stroke-dashoffset:1;animation:wm 2s {EASE} forwards}}"
        "@keyframes wm{45%{stroke-dashoffset:0;fill-opacity:0}"
        "75%{fill-opacity:1;stroke-opacity:.6}"
        "100%{stroke-dashoffset:0;fill-opacity:1;stroke-opacity:0}}"
        f".sheen{{animation:sheen 7s {EASE} 3s infinite;transform:translateX(-300px)}}"
        f"@keyframes sheen{{0%{{transform:translateX(-300px)}}"
        f"45%,100%{{transform:translateX({WIDTH + 100}px)}}}}"
        ".rise{opacity:0;animation:rise .9s ease 1.3s forwards}"
        "@keyframes rise{to{opacity:1}}"
        f".thread{{stroke-dasharray:{inner};stroke-dashoffset:{inner};"
        f"animation:thread 1.6s {EASE} 1.5s forwards}}"
        "@keyframes thread{to{stroke-dashoffset:0}}"
        f".pulse{{opacity:0;animation:pulse 7s {EASE} 3.2s infinite}}"
        f"@keyframes pulse{{0%{{opacity:0;transform:translateX(0)}}5%{{opacity:1}}"
        f"45%{{opacity:1}}50%{{opacity:0;transform:translateX({inner}px)}}"
        f"100%{{opacity:0;transform:translateX({inner}px)}}}}"
        f".ph{{opacity:0;animation:ph {CYCLE}s linear infinite}}"
        "@keyframes ph{0%{opacity:0;transform:translateY(6px)}"
        "2.5%,22%{opacity:1;transform:none}24.5%,100%{opacity:0}}"
        f".lay{{fill:{t.panel};stroke:{t.faint};stroke-width:1}}"
        f".lit{{fill:{t.accent};fill-opacity:.28;stroke:{t.mint};stroke-width:1.4;"
        f"opacity:0;animation:lit {CYCLE}s linear infinite}}"
        "@keyframes lit{0%{opacity:0}2.5%,22%{opacity:1}24.5%,100%{opacity:0}}",
        ".wm{animation:none;fill-opacity:1;stroke-opacity:0}"
        ".sheen,.pulse,.lit{animation:none}"
        ".pulse{opacity:0}"
        ".rise{animation:none;opacity:1}"
        ".thread{animation:none;stroke-dashoffset:0}"
        ".ph{animation:none}.ph0{opacity:1}"
        ".lit{opacity:0}",
    )

    wordmark = _wordmark(doc, inner)
    doc.add(
        '<g clip-path="url(#frame)">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="{t.bg}"/>',
        f'<rect x="-60" y="-60" width="{WIDTH + 120}" height="{HEIGHT + 120}" fill="url(#halo)"/>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#dots)"/>',
        "</g>",
        f'<rect x=".5" y=".5" width="{WIDTH - 1}" height="{HEIGHT - 1}" rx="16" '
        f'stroke="{t.stroke}"/>',
        '<g class="rise">',
        doc.label_text(MARGIN, 54, HEADLINE, "muted", size=12, track=2.2),
        "</g>",
        wordmark,
        '<g clip-path="url(#wclip)"><rect class="sheen" y="66" width="240" height="160" '
        'fill="url(#sheen)"/></g>',
        f'<line class="thread" x1="{MARGIN}" y1="{RULE_Y}" x2="{WIDTH - MARGIN}" y2="{RULE_Y}" '
        f'stroke="url(#aurora)" stroke-width="2"/>',
        f'<circle class="pulse" cx="{MARGIN}" cy="{RULE_Y}" r="3.5" fill="{t.gleam}"/>',
        '<g class="rise">',
        doc.text(MARGIN, 272, TAGLINE, "sans", 300, 27, "ink", track=-0.2),
        _layer_stack(doc),
        _layer_copy(doc),
        f'<circle cx="{MARGIN + 4}" cy="370" r="4" fill="{t.mint}"/>',
        doc.label_text(MARGIN + 22, 374, STATUS, "muted", size=11.5, track=1.8),
        "</g>",
    )
    return doc.render()
