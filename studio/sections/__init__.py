"""Renderers for every asset on the profile. Each returns a finished SVG string."""

from __future__ import annotations

from pathlib import Path

from ..content import CLIENTS, PROJECTS
from ..theme import THEMES
from . import architecture, chrome, clients, code, hero, projects, stack


def render_all(out_dir: Path) -> int:
    """Write the dark and light variant of every asset and return the file count."""
    written = 0
    for theme in THEMES:
        assets = {
            "hero": hero.render(theme),
            "architecture": architecture.render(theme),
            "code": code.render(theme),
            "stack": stack.render(theme),
            "divider": chrome.divider(theme),
            "contact": chrome.contact(theme),
            "footer": chrome.footer(theme),
            "work-heading": chrome.heading(theme, "04", "SELECTED WORK", "CLICK A CARD TO OPEN IT"),
        }
        assets["clients-heading"] = chrome.heading(theme, "05", "CLIENT WORK", "DESIGN & WEB")
        assets["client-case-studies"] = clients.case_studies(theme)
        for i, client in enumerate(CLIENTS):
            assets[f"client-{client.slug}"] = clients.card(theme, client, i % 2 == 0)
        for project in PROJECTS:
            assets[f"project-{project.slug}"] = projects.render(theme, project)
        for i, (name, label) in enumerate(chrome.BUTTONS):
            assets[f"btn-{name}"] = chrome.button(theme, name, label, first=i == 0)
        for name, svg in assets.items():
            (out_dir / f"{name}-{theme.name}.svg").write_text(svg, encoding="utf-8")
            written += 1
    return written
