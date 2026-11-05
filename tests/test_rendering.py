import ast
import re
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from studio.content import CLIENTS, SNIPPETS
from studio.sections import render_all
from studio.sections.code import tokenize

ROOT = Path(__file__).resolve().parent.parent
SVG = "{http://www.w3.org/2000/svg}"


@pytest.fixture(scope="module")
def rendered(tmp_path_factory):
    out = tmp_path_factory.mktemp("assets")
    render_all(out)
    return {path.name: path.read_text(encoding="utf-8") for path in out.glob("*.svg")}


def test_every_asset_ships_in_both_themes(rendered):
    stems = {name.rsplit("-", 1)[0] for name in rendered}
    assert len(rendered) == 2 * len(stems)
    for stem in stems:
        assert f"{stem}-dark.svg" in rendered
        assert f"{stem}-light.svg" in rendered


def test_assets_are_well_formed_and_labelled(rendered):
    for name, svg in rendered.items():
        root = ET.fromstring(svg)
        assert root.tag == f"{SVG}svg", name
        assert root.get("role") == "img", name
        assert root.get("aria-label"), name
        assert root.find(f"{SVG}title") is not None, name


def test_assets_are_self_contained(rendered):
    """GitHub's image sandbox blocks scripts and any external resource."""
    for name, svg in rendered.items():
        assert "<script" not in svg, name
        assert "@import" not in svg, name
        external = re.findall(r'(?:href|src)="(?!#)([^"]+)"', svg)
        assert not external, (name, external)


def test_every_glyph_reference_resolves(rendered):
    for name, svg in rendered.items():
        ids = set(re.findall(r'\bid="([^"]+)"', svg))
        refs = set(re.findall(r'href="#([^"]+)"', svg))
        assert refs <= ids, name


def test_motion_is_css_and_honours_reduced_motion(rendered):
    for name, svg in rendered.items():
        assert "<animate" not in svg, name
        if "infinite" in svg:
            assert "prefers-reduced-motion" in svg, name


def test_readme_only_references_assets_that_exist():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for reference in set(re.findall(r"\./assets/[\w-]+\.svg", readme)):
        assert (ROOT / reference).is_file(), reference


def test_tokenizer_classifies_tokens():
    kinds = {
        text: kind for _, text, kind in tokenize('return fetch("/x", 14); // done', "typescript")
    }
    assert kinds["return"] == "keyword"
    assert kinds["fetch"] == "call"
    assert kinds['"/x"'] == "string"
    assert kinds["14"] == "number"
    assert kinds["// done"] == "comment"


def test_python_snippet_parses():
    source = next(code for _, language, code in SNIPPETS if language == "python")
    ast.parse(source)


def test_readme_links_every_client_in_tight_rows():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for client in CLIENTS:
        assert f'<a href="{client.url}">' in readme, client.slug
    # Whitespace between two 50% images would push the second one onto a new line.
    assert re.search(r'client-cassinil-dark\.svg" width="50%"></picture></a><a ', readme)
    assert re.search(r'client-rune-dark\.svg" width="50%"></picture></a><a ', readme)
