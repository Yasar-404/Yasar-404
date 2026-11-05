"""Command line entry point: `python -m studio sync|build|all`."""

from __future__ import annotations

import argparse
from pathlib import Path

from .analytics import compute
from .content import GITHUB_USER
from .github import fetch_snapshot, load_snapshot, save_snapshot
from .sections import render_all

ROOT = Path(__file__).resolve().parent.parent
SNAPSHOT = ROOT / "data" / "snapshot.json"
ASSETS = ROOT / "assets"


def sync() -> None:
    snapshot = fetch_snapshot(GITHUB_USER)
    save_snapshot(snapshot, SNAPSHOT)
    print(f"synced {len(snapshot['repositories'])} repositories")


def build() -> None:
    metrics = compute(load_snapshot(SNAPSHOT))
    ASSETS.mkdir(exist_ok=True)
    written = render_all(metrics, ASSETS)
    print(f"rendered {written} assets from {metrics.commits} commits")


def main() -> None:
    parser = argparse.ArgumentParser(prog="studio", description=__doc__)
    parser.add_argument("command", choices=("sync", "build", "all"))
    command = parser.parse_args().command
    if command in ("sync", "all"):
        sync()
    if command in ("build", "all"):
        build()


if __name__ == "__main__":
    main()
