"""Client work as a two-column grid of linked cards, each with a motif from its industry.

Each card is half of the page canvas. Left and right cards carry different outer margins,
so the grid lines up with the full-width panels when the README places them side by side.
"""

from __future__ import annotations

from ..content import Client
from ..svg import EASE, MARGIN, WIDTH, Doc
from ..theme import Theme

CARD_CANVAS_W = WIDTH // 2
CARD_W = CARD_CANVAS_W - MARGIN - 8
CARD_CANVAS_H = 176
STRIP_H = 72
LOOP = 8


def _arrow(doc: Doc, x: float, y: float) -> str:
    """A small arrow signalling that the card is a link."""
    stroke = f'stroke="{doc.theme.accent}" stroke-width="1.6" stroke-linecap="round"'
    return (
        f'<g transform="translate({x} {y})">'
        f'<path d="M0 0 H12 M7 -5 L12 0 7 5" {stroke} stroke-linejoin="round"/></g>'
    )


def _draw_css(doc: Doc) -> None:
    doc.style(
        f".draw{{stroke-dasharray:1;animation:draw {LOOP}s {EASE} infinite}}"
        "@keyframes draw{0%{stroke-dashoffset:1}35%,88%{stroke-dashoffset:0}"
        "100%{stroke-dashoffset:1}}",
        ".draw{animation:none;stroke-dashoffset:0}",
    )


def _blueprint(doc: Doc) -> str:
    """A building elevation drawing itself on a drafting grid."""
    t = doc.theme
    _draw_css(doc)
    grid = "".join(
        f'<path d="M{i * 16} 0 V80 M0 {i * 16} H96" stroke="{t.stroke}"/>' for i in range(6)
    )
    return (
        grid + f'<path class="draw" pathLength="1" d="M12 76 V32 H44 V14 H78 V76 Z" '
        f'stroke="{t.accent}" stroke-width="1.6" stroke-linejoin="round"/>'
        f'<path class="draw" pathLength="1" style="animation-delay:.5s" '
        f'd="M22 44 h12 M22 56 h12 M54 26 h14 M54 40 h14 M54 54 h14 M54 76 v-10 h14 v10" '
        f'stroke="{t.mint}" stroke-width="1.4"/>'
    )


def _pulse(doc: Doc) -> str:
    """A heart-rate trace."""
    t = doc.theme
    _draw_css(doc)
    return (
        f'<path d="M0 44 H96" stroke="{t.stroke}"/>'
        f'<path class="draw" pathLength="1" d="M0 44 H24 L32 44 L38 22 L47 70 L55 32 L60 44 H96" '
        f'stroke="{t.mint}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'
    )


def _gallery(doc: Doc) -> str:
    """Arched openings lighting up in turn, like walking through a studio."""
    t = doc.theme
    doc.style(
        f".arch{{opacity:0;animation:arch {LOOP}s ease-in-out infinite}}"
        "@keyframes arch{0%,30%{opacity:1}42%,100%{opacity:0}}",
        ".arch{animation:none;opacity:0}",
    )
    shape = "M{x} 76 V34 a12 12 0 0 1 24 0 V76 Z"
    parts = [f'<path d="M0 76 H96" stroke="{t.faint}"/>']
    for i, x in enumerate((6, 36, 66)):
        d = shape.format(x=x)
        parts.append(f'<path d="{d}" stroke="{t.faint}"/>')
        parts.append(
            f'<path class="arch" style="animation-delay:{i * 2.6:.1f}s" d="{d}" '
            f'fill="{t.accent}" fill-opacity=".25" stroke="{t.accent}" stroke-width="1.4"/>'
        )
    return "".join(parts)


def _bloom(doc: Doc) -> str:
    """Petals opening and closing slowly."""
    t = doc.theme
    doc.style(
        ".petals{transform-box:view-box;transform-origin:48px 42px;"
        f"animation:bloom {LOOP}s ease-in-out infinite}}"
        "@keyframes bloom{0%,100%{transform:rotate(-14deg) scale(.82)}"
        "50%{transform:rotate(14deg) scale(1)}}",
        ".petals{animation:none}",
    )
    petals = "".join(
        f'<ellipse cx="48" cy="20" rx="10" ry="22" transform="rotate({a} 48 42)" '
        f'fill="{t.mint}" fill-opacity=".1" stroke="{t.mint}" stroke-width="1.3"/>'
        for a in range(0, 360, 60)
    )
    return f'<g class="petals">{petals}</g><circle cx="48" cy="42" r="4" fill="{t.accent}"/>'


MOTIFS = {"blueprint": _blueprint, "pulse": _pulse, "gallery": _gallery, "bloom": _bloom}


def card(theme: Theme, client: Client, left_column: bool) -> str:
    doc = Doc(theme, f"{client.name}: {client.summary}", CARD_CANVAS_H, CARD_CANVAS_W)
    x = MARGIN if left_column else 8
    pad = x + 22
    doc.add(
        f'<rect class="card" x="{x}" y="6" width="{CARD_W}" height="{CARD_CANVAS_H - 12}" '
        'rx="14"/>',
        doc.label_text(pad, 38, client.industry, "accent", size=10, track=1.8),
        doc.text(pad, 74, client.name, "sans", 600, 21, "ink", track=-0.2),
        doc.text(pad, 100, client.summary, "sans", 400, 13, "muted"),
        doc.label_text(pad, 148, client.tools, "faint", size=10, track=1.3),
        _arrow(doc, x + CARD_W - 36, 144),
        f'<g transform="translate({x + CARD_W - 118} 22)">{MOTIFS[client.motif](doc)}</g>',
    )
    return doc.render()


def case_studies(theme: Theme) -> str:
    doc = Doc(theme, "Read the full case studies on Behance", STRIP_H)
    doc.add(
        f'<rect class="card" x="{MARGIN}" y="6" width="{WIDTH - 2 * MARGIN}" '
        f'height="{STRIP_H - 12}" rx="14"/>',
        doc.text(MARGIN + 22, 41, "Read the full case studies", "sans", 500, 15, "ink"),
        doc.label_text(WIDTH - MARGIN - 60, 40, "BEHANCE", "muted", "end", 10.5, 2),
        _arrow(doc, WIDTH - MARGIN - 44, 36),
    )
    return doc.render()
