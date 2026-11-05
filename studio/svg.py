"""A small SVG document builder with outlined text.

Motion rules that follow from how GitHub displays images:

* Animation only starts on page load, so anything below the fold must loop.
  One-shot entrances are reserved for the hero.
* All motion is CSS rather than SMIL, because `prefers-reduced-motion` cannot
  stop SMIL. Each asset defines a calm, complete resting state.
"""

from __future__ import annotations

from html import escape

from .theme import Theme
from .typography import face

WIDTH = 960
MARGIN = 48
EASE = "cubic-bezier(.4,0,.2,1)"


def num(value: float) -> str:
    text = f"{value:.2f}".rstrip("0").rstrip(".")
    return text if text not in ("", "-0") else "0"


class Doc:
    def __init__(self, theme: Theme, label: str, height: int, width: int = WIDTH) -> None:
        self.theme = theme
        self.label = label
        self.width = width
        self.height = height
        self.rules: list[str] = []
        self.reduced: list[str] = []
        self.defs: list[str] = []
        self.body: list[str] = []
        self._glyph_ids: dict[tuple, str] = {}

    def add(self, *markup: str) -> None:
        self.body.extend(markup)

    def style(self, css: str, reduced: str = "") -> None:
        self.rules.append(css)
        if reduced:
            self.reduced.append(reduced)

    def define(self, markup: str) -> None:
        self.defs.append(markup)

    def _glyph_ref(self, family: str, weight: int, glyph: str, path: str) -> str:
        key = (family, weight, glyph)
        if key not in self._glyph_ids:
            ref = f"g{len(self._glyph_ids):x}"
            self._glyph_ids[key] = ref
            self.defs.append(f'<path id="{ref}" d="{path}"/>')
        return self._glyph_ids[key]

    def text(
        self,
        x: float,
        y: float,
        content: str,
        family: str = "sans",
        weight: int = 400,
        size: float = 14,
        cls: str = "ink",
        anchor: str = "start",
        track: float = 0.0,
    ) -> str:
        """Return outlined text. `track` is extra spacing per glyph, in pixels."""
        f = face(family, weight)
        scale = size / f.upm
        width = f.width(content, size, track)
        if anchor == "end":
            x -= width - track
        elif anchor == "middle":
            x -= (width - track) / 2

        uses, cursor = [], 0.0
        for char in content:
            glyph = f.glyph(char)
            path = f.path(glyph)
            if path:
                ref = self._glyph_ref(family, weight, glyph, path)
                at = f' x="{round(cursor)}"' if cursor else ""
                uses.append(f'<use href="#{ref}"{at}/>')
            cursor += f.advances[glyph] + track / scale

        return (
            f'<g class="{cls}" transform="translate({num(x)} {num(y)}) '
            f'scale({scale:.5f} {-scale:.5f})">{"".join(uses)}</g>'
        )

    def label_text(
        self,
        x: float,
        y: float,
        content: str,
        cls: str = "muted",
        anchor: str = "start",
        size: float = 11.5,
        track: float = 2.2,
    ) -> str:
        return self.text(x, y, content, "mono", 500, size, cls, anchor, track)

    def section_header(self, index: str, title: str, meta: str = "") -> str:
        parts = [
            self.text(MARGIN, 44, index, "mono", 700, 12.5, "accent", track=1.5),
            f'<line class="rule" x1="{MARGIN + 28}" y1="40" x2="{MARGIN + 66}" y2="40"/>',
            self.label_text(MARGIN + 78, 44, title, "ink", size=12.5, track=3),
        ]
        if meta:
            parts.append(self.label_text(WIDTH - MARGIN, 44, meta, "faint", "end", 10.5, 1.6))
        return "".join(parts)

    def _base_css(self) -> str:
        t = self.theme
        return (
            f".ink{{fill:{t.ink}}}.muted{{fill:{t.muted}}}.faint{{fill:{t.faint}}}"
            f".accent{{fill:{t.accent}}}.mintf{{fill:{t.mint}}}"
            f".rule{{stroke:{t.stroke};stroke-width:1}}"
            f".card{{fill:{t.panel};stroke:{t.stroke};stroke-width:1}}"
        )

    def render(self) -> str:
        title = escape(self.label, quote=True)
        reduced = ""
        if self.reduced:
            reduced = f"@media(prefers-reduced-motion:reduce){{{''.join(self.reduced)}}}"
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" '
            f'height="{self.height}" viewBox="0 0 {self.width} {self.height}" fill="none" '
            f'role="img" aria-label="{title}"><title>{title}</title>'
            f"<defs><style>{self._base_css()}{''.join(self.rules)}{reduced}</style>"
            f"{''.join(self.defs)}</defs>{''.join(self.body)}</svg>\n"
        )
