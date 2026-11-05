"""Outline text to vector glyphs.

GitHub serves README images in a sandbox that cannot load web fonts, and system
font stacks differ per OS, which breaks any layout that depends on text width.
Outlining gives identical type everywhere. Each glyph is defined once per document
and reused, so files stay small even for long code listings.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import cache
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).resolve().parent.parent / "fonts"

FACES = {
    ("sans", 300): "inter-latin-300-normal.woff",
    ("sans", 400): "inter-latin-400-normal.woff",
    ("sans", 500): "inter-latin-500-normal.woff",
    ("sans", 600): "inter-latin-600-normal.woff",
    ("mono", 400): "jetbrains-mono-latin-400-normal.woff",
    ("mono", 500): "jetbrains-mono-latin-500-normal.woff",
    ("mono", 700): "jetbrains-mono-latin-700-normal.woff",
    ("display", 800): "unbounded-latin-800-normal.woff",
}


@dataclass
class Face:
    key: tuple[str, int]
    upm: int
    cmap: dict[int, str]
    advances: dict[str, int]
    glyph_set: object
    _paths: dict[str, str] = field(default_factory=dict)

    def glyph(self, char: str) -> str:
        try:
            return self.cmap[ord(char)]
        except KeyError:
            raise ValueError(f"{char!r} is not in font subset {self.key}") from None

    def path(self, glyph_name: str) -> str:
        if glyph_name not in self._paths:
            pen = SVGPathPen(self.glyph_set, ntos=lambda v: str(round(v)))
            self.glyph_set[glyph_name].draw(pen)
            self._paths[glyph_name] = pen.getCommands()
        return self._paths[glyph_name]

    def width(self, text: str, size: float, track: float = 0.0) -> float:
        units = sum(self.advances[self.glyph(c)] for c in text)
        return units * size / self.upm + track * len(text)


@cache
def face(family: str, weight: int) -> Face:
    font = TTFont(FONT_DIR / FACES[(family, weight)])
    return Face(
        key=(family, weight),
        upm=font["head"].unitsPerEm,
        cmap=font.getBestCmap(),
        advances={name: adv for name, (adv, _) in font["hmtx"].metrics.items()},
        glyph_set=font.getGlyphSet(),
    )
