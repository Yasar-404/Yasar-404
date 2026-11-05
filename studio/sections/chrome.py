"""Connective tissue: divider, contact heading, footer and link buttons."""

from __future__ import annotations

from ..svg import EASE, MARGIN, WIDTH, Doc
from ..theme import Theme
from ..typography import face

BUTTON_H, BUTTON_GAP = 50, 10

BUTTONS = (
    ("portfolio", "Portfolio"),
    ("email", "Email"),
    ("github", "GitHub"),
    ("behance", "Behance"),
)


def divider(theme: Theme) -> str:
    t = theme
    doc = Doc(t, "Section divider", 40)
    span = WIDTH - 2 * MARGIN
    doc.style(
        f".tick{{animation:tick 7s {EASE} infinite}}"
        f"@keyframes tick{{0%{{transform:translateX(0);opacity:0}}8%,92%{{opacity:1}}"
        f"100%{{transform:translateX({span}px);opacity:0}}}}",
        ".tick{animation:none;opacity:0}",
    )
    doc.add(
        f'<line class="rule" x1="{MARGIN}" y1="20" x2="{WIDTH - MARGIN}" y2="20"/>',
        f'<circle class="tick" cx="{MARGIN}" cy="20" r="2.5" fill="{t.accent}"/>',
    )
    return doc.render()


def contact(theme: Theme) -> str:
    t = theme
    doc = Doc(t, "Contact: open to full-stack and software engineering roles", 150)
    doc.add(
        doc.section_header("06", "CONTACT"),
        f'<circle cx="{WIDTH - MARGIN - 4}" cy="40" r="4" fill="{t.mint}"/>',
        doc.label_text(WIDTH - MARGIN - 18, 44, "AVAILABLE", "muted", "end", 11, 1.8),
        doc.text(
            MARGIN, 96, "Let's build something that holds up.", "sans", 300, 30, "ink", track=-0.3
        ),
        doc.text(
            MARGIN,
            124,
            "Open to full-stack and software engineering roles, and select product work.",
            "sans",
            400,
            15,
            "muted",
        ),
    )
    return doc.render()


def footer(theme: Theme) -> str:
    t = theme
    doc = Doc(t, "Yasar K, Chennai, India", 64)
    doc.add(
        f'<line class="rule" x1="{MARGIN}" y1="8" x2="{WIDTH - MARGIN}" y2="8"/>',
        f'<path d="M{MARGIN + 6} 30 l6 6 -6 6 -6 -6 Z" fill="{t.accent}"/>',
        doc.label_text(MARGIN + 22, 41, "YASAR K", "ink", size=11.5, track=2.4),
        doc.label_text(
            WIDTH / 2, 41, "RENDERED IN PYTHON  ·  TESTED IN CI", "faint", "middle", 10.5, 1.6
        ),
        doc.label_text(WIDTH - MARGIN, 41, "CHENNAI, IN", "faint", "end", 10.5, 1.6),
    )
    return doc.render()


def _button_icon(name: str, t: Theme) -> str:
    stroke = (
        f'stroke="{t.accent}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    )
    return {
        "portfolio": f'<circle r="7" {stroke}/><path {stroke} d="M-7 0 H7 M0 -7 q4 7 0 14 q-4 -7 0 -14"/>',
        "email": f'<rect x="-8" y="-6" width="16" height="12" rx="2.5" {stroke}/>'
        f'<path {stroke} d="M-7 -4 L0 1 7 -4"/>',
        "github": f'<circle cx="-4" cy="-5" r="2" {stroke}/><circle cx="-4" cy="6" r="2" {stroke}/>'
        f'<circle cx="5" cy="-3" r="2" {stroke}/><path {stroke} d="M-4 -3 V4 M5 -1 q0 3 -9 4"/>',
        "behance": f'<path {stroke} d="M-8 -5 H-3 q3 0 3 2.5 t-3 2.5 H-8 Z M-8 0 H-2 q3 0 3 2.5 '
        f't-3 2.5 H-8 Z M3 -5 H8"/>',
    }[name]


def button_canvas_width(label: str, first: bool) -> int:
    """Width of a button's image: the pill, its right gap and, for the first, the page margin."""
    pill = round(46 + face("mono", 500).width(label, 14) + 22)
    return pill + BUTTON_GAP + (MARGIN if first else 0)


def button(theme: Theme, name: str, label: str, first: bool) -> str:
    """Render one button on the page grid, so the README can size it as a share of the column."""
    t = theme
    left = MARGIN if first else 0
    width = button_canvas_width(label, first)
    doc = Doc(t, label, BUTTON_H, width)
    doc.add(
        f'<rect class="card" x="{left + 0.5}" y=".5" width="{width - left - BUTTON_GAP - 1}" '
        f'height="{BUTTON_H - 1}" rx="12"/>',
        f'<g transform="translate({left + 24} {BUTTON_H / 2})">{_button_icon(name, t)}</g>',
        doc.text(left + 46, BUTTON_H / 2 + 5, label, "mono", 500, 14, "ink"),
    )
    return doc.render()


def heading(theme: Theme, index: str, title: str, meta: str = "") -> str:
    doc = Doc(theme, title.capitalize(), 56)
    doc.add(doc.section_header(index, title, meta))
    return doc.render()
