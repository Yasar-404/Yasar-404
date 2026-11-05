"""The stack grouped by layer, using an original line-icon set. No trademarked logos."""

from __future__ import annotations

import math

from ..content import STACK
from ..svg import MARGIN, WIDTH, Doc
from ..theme import Theme

ROW_H = 106
TOP = 74
HEIGHT = TOP + len(STACK) * ROW_H + 8
LOOP = 14


def _hexagon(radius: float) -> str:
    return " ".join(
        f"{radius * math.cos(math.radians(a)):.1f},{radius * math.sin(math.radians(a)):.1f}"
        for a in range(-90, 270, 60)
    )


def _monogram(doc: Doc, letters: str, size: float = 14) -> str:
    return doc.text(0, size * 0.36, letters, "mono", 700, size, "iconfill", "middle")


def icon(doc: Doc, name: str) -> str:
    """Return a glyph drawn around (0, 0) with a radius of about 13."""
    table = {
        "React": '<ellipse rx="13" ry="5" class="ic" transform="rotate(-30)"/>'
        '<ellipse rx="13" ry="5" class="ic" transform="rotate(30)"/>'
        '<circle r="2.4" class="iconfill"/>'
        '<circle cx="13" r="2" class="mintf"/>',
        "Next.js": '<circle r="12" class="ic"/>'
        '<path class="ic" d="M-5 6 V-6 L6 8"/><path class="ica" d="M5 -6 V2"/>',
        "TypeScript": '<rect x="-12" y="-12" width="24" height="24" rx="5" class="ic"/>'
        '<path class="ic" d="M-8 -3 H1 M-3.5 -3 V7"/>'
        '<path class="ica" d="M9 -2 q-1 -1.6 -3 -1.4 -2.4 .2 -2.4 2.2 0 1.8 2.6 2.4 2.8 .6 2.8 2.6 '
        '0 2 -2.6 2 -2.2 0 -3.2 -1.6"/>',
        "JavaScript": '<path class="ic" d="M-5 -12 q-5 0 -5 5 v3 q0 4 -4 4 4 0 4 4 v3 q0 5 5 5"/>'
        '<path class="ica" d="M5 -12 q5 0 5 5 v3 q0 4 4 4 -4 0 -4 4 v3 q0 5 -5 5"/>',
        "Tailwind": '<path class="ic" d="M-13 -2 q4 -7 9 -4 t8 1 q4 0 8 -4 -3 8 -8 6 t-8 -2 q-5 -1 -9 3 Z"/>'
        '<path class="ica" d="M-13 7 q4 -7 9 -4 t8 1 q4 0 8 -4 -3 8 -8 6 t-8 -2 q-5 -1 -9 3 Z"/>',
        "Motion": '<path class="ic" d="M-13 9 C-4 9 -4 -9 13 -9"/>'
        '<circle cx="13" cy="-9" r="3" class="mintf"/>',
        "Python": '<path class="ic" d="M0 0 H-8 q-4 0 -4 -4 v-3 q0 -5 5 -5 h6 q5 0 5 5 V-1 q0 1 -1 1"/>'
        '<path class="ica" d="M0 0 H8 q4 0 4 4 v3 q0 5 -5 5 H1 q-5 0 -5 -5 V1 q0 -1 1 -1"/>'
        '<circle cx="-4" cy="-8" r="1.3" class="iconfill"/>'
        '<circle cx="4" cy="8" r="1.3" class="mintf"/>',
        "Java": '<path class="ic" d="M-11 -1 H8 V5 q0 6 -6 6 h-7 q-6 0 -6 -6 Z"/>'
        '<path class="ic" d="M8 1 h2 q4 0 4 3 0 3 -4 3 h-2"/>'
        '<path class="ica" d="M-5 -6 q-2 -2 0 -4 q2 -2 0 -4"/>'
        '<path class="ica" d="M1 -6 q-2 -2 0 -4 q2 -2 0 -4"/>',
        "Node.js": f'<polygon points="{_hexagon(13)}" class="ic"/>'
        '<path class="ica" d="M-5 4 V-4 L5 4 V-4"/>',
        "Go": _monogram(doc, "Go", 15),
        "REST APIs": '<path class="ic" d="M-13 -5 H9 M4 -10 l5 5 -5 5"/>'
        '<path class="ica" d="M13 5 H-9 M-4 0 l-5 5 5 5"/>',
        "Prisma": '<path class="ic" d="M1 -13 L12 9 -5 13 -12 3 Z"/>'
        '<path class="ica" d="M1 -13 L-5 13"/>',
        "SQL": '<rect x="-12" y="-11" width="24" height="22" rx="3" class="ic"/>'
        '<path class="ic" d="M-12 -4 H12 M-12 3 H12 M-4 -11 V11"/>'
        '<rect class="mintf" x="-12" y="-4" width="24" height="7" fill-opacity=".4"/>',
        "PostgreSQL": '<ellipse cy="-8" rx="11" ry="4" class="ic"/>'
        '<path class="ic" d="M-11 -8 V8 q0 4 11 4 11 0 11 -4 V-8"/>'
        '<path class="ica" d="M-11 0 q0 4 11 4 11 0 11 -4"/>',
        "Netlify": '<polygon points="0,-13 13,0 0,13 -13,0" class="ic"/>'
        '<path class="ica" d="M-5 0 H5 M0 -5 V5"/>',
        "Git": '<path class="ic" d="M-6 12 V-12"/><path class="ica" d="M-6 6 q0 -6 6 -6 h1"/>'
        '<circle cx="-6" cy="12" r="2.5" class="iconfill"/>'
        '<circle cx="-6" cy="-12" r="2.5" class="iconfill"/>'
        '<circle cx="6" cy="0" r="3" class="mintf"/>',
        "GitHub Actions": '<circle cx="-9" cy="-7" r="4" class="ic"/><circle cx="9" cy="7" r="4" '
        'class="ica"/><path class="ic" d="M-9 -3 V3 q0 4 4 4 H5"/><path class="ic" d="M-5 -7 H9 V3"/>',
        "Vercel": '<path class="ic" d="M0 -11 L13 11 H-13 Z"/><path class="ica" d="M-5 11 L0 2 5 11"/>',
        "Figma": '<rect x="-8" y="-13" width="8" height="8.6" rx="4" class="ic"/>'
        '<rect x="0" y="-13" width="8" height="8.6" rx="4" class="ic"/>'
        '<rect x="-8" y="-4.4" width="8" height="8.6" rx="4" class="ic"/>'
        '<circle cx="4" cy="-.1" r="4" class="ica"/>'
        '<path class="ic" d="M-8 8.2 a4 4 0 0 1 4 -4 h4 v4.3 a4 4 0 0 1 -8 0 Z"/>',
        "Framer": '<path class="ic" d="M-9 -12 H9 V-3 H0 Z"/><path class="ica" d="M-9 -3 H9 V6 H0 Z"/>'
        '<path class="ic" d="M-9 -3 V6 L0 13 V6"/>',
        "Webflow": '<path class="ic" d="M-13 -7 L-7 8 -1 -4 3 8 13 -9"/>',
        "Illustrator": '<rect x="-12" y="-12" width="24" height="24" rx="5" class="ic"/>'
        + _monogram(doc, "Ai", 12),
        "Photoshop": '<rect x="-12" y="-12" width="24" height="24" rx="5" class="ic"/>'
        + _monogram(doc, "Ps", 12),
        "Design Systems": '<rect x="-12" y="-12" width="10" height="10" rx="2" class="ic"/>'
        '<rect x="2" y="-12" width="10" height="10" rx="5" class="ica"/>'
        '<rect x="-12" y="2" width="10" height="10" rx="5" class="ica"/>'
        '<rect x="2" y="2" width="10" height="10" rx="2" class="ic"/>',
    }
    return table[name]


def render(theme: Theme) -> str:
    names = ", ".join(n for _, items in STACK for n in items)
    doc = Doc(theme, f"Technology stack: {names}", HEIGHT)
    t = theme
    doc.style(
        f".ic{{stroke:{t.ink};stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}}"
        f".ica{{stroke:{t.accent};stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round}}"
        f".iconfill{{fill:{t.ink}}}"
        f".tile{{fill:{t.panel};stroke:{t.stroke}}}"
        f".tlit{{stroke:{t.accent};stroke-width:1.5;fill:{t.accent};fill-opacity:.1;opacity:0;"
        f"animation:tlit {LOOP}s ease-in-out infinite}}"
        "@keyframes tlit{0%{opacity:0}2%,7%{opacity:1}12%,100%{opacity:0}}",
        ".tlit{animation:none;opacity:0}",
    )
    doc.add(doc.section_header("03", "THE STACK", "FROM INTERFACE TO INDEX"))

    index = 0
    total = sum(len(items) for _, items in STACK)
    for r, (group, items) in enumerate(STACK):
        y = TOP + r * ROW_H
        doc.add(
            doc.label_text(MARGIN, y + 8, group, "faint", size=10.5, track=2.2),
            f'<line class="rule" x1="{MARGIN + 170}" y1="{y + 4}" x2="{WIDTH - MARGIN}" '
            f'y2="{y + 4}"/>',
        )
        cell = (WIDTH - 2 * MARGIN) / len(items)
        for c, name in enumerate(items):
            cx = MARGIN + cell * (c + 0.5)
            cy = y + 44
            delay = index / total * LOOP
            doc.add(
                f'<rect class="tile" x="{cx - 22:.1f}" y="{cy - 22}" width="44" height="44" rx="12"/>',
                f'<rect class="tlit" style="animation-delay:{delay:.2f}s" x="{cx - 22:.1f}" '
                f'y="{cy - 22}" width="44" height="44" rx="12"/>',
                f'<g transform="translate({cx:.1f} {cy})">{icon(doc, name)}</g>',
                doc.text(cx, cy + 40, name, "sans", 500, 12.5, "muted", "middle"),
            )
            index += 1
    return doc.render()
