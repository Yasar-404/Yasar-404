"""Design tokens. Every colour in every asset comes from here."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    name: str
    bg: str
    panel: str
    ink: str
    muted: str
    faint: str
    stroke: str
    dot: str
    gleam: str
    accent: str
    iris: str
    mint: str
    # Syntax colours for the code panel.
    keyword: str
    string: str
    type: str
    number: str
    comment: str


DARK = Theme(
    name="dark",
    bg="#0A0A0B",
    panel="#101014",
    ink="#EDEDF0",
    muted="#9A9AA4",
    faint="#6F6F79",
    stroke="#26262C",
    dot="#1C1C21",
    gleam="#FFFFFF",
    accent="#6E8BFF",
    iris="#7C7BF7",
    mint="#43E7C4",
    keyword="#8FA3FF",
    string="#5FE3C6",
    type="#E9C07B",
    number="#F0957F",
    comment="#70707C",
)

LIGHT = Theme(
    name="light",
    bg="#FBFBFD",
    panel="#F3F3F7",
    ink="#16161A",
    muted="#5F5F6A",
    faint="#85858F",
    stroke="#E0E0E6",
    dot="#E6E6EC",
    gleam="#5B6BFF",
    accent="#4A63E8",
    iris="#5F5EE0",
    mint="#0E9E80",
    keyword="#3F54D6",
    string="#0B8770",
    type="#A5650C",
    number="#C24A32",
    comment="#85858F",
)

THEMES = (DARK, LIGHT)
