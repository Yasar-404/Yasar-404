"""Command line entry point: `python -m studio`."""

from __future__ import annotations

from pathlib import Path

from .sections import render_all

ASSETS = Path(__file__).resolve().parent.parent / "assets"


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    print(f"rendered {render_all(ASSETS)} assets")


if __name__ == "__main__":
    main()
