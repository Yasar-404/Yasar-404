"""Load a snapshot into SQLite and answer every metric with SQL."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path

SQL_DIR = Path(__file__).parent / "sql"


@dataclass(frozen=True)
class Metrics:
    commits: int
    active_days: int
    repositories: int
    first_commit: str | None
    last_commit: str | None
    longest_streak: int
    daily: dict[str, int]
    languages: list[tuple[str, float]]


def _sql(name: str) -> str:
    return (SQL_DIR / f"{name}.sql").read_text(encoding="utf-8")


def load(snapshot: dict) -> sqlite3.Connection:
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(_sql("schema"))
    with db:
        for repo in snapshot["repositories"]:
            db.execute(
                "INSERT INTO repositories VALUES (?, ?, ?, ?)",
                (repo["name"], repo["description"], repo["homepage"], repo["pushed_at"]),
            )
            db.executemany(
                "INSERT INTO language_bytes VALUES (?, ?, ?)",
                [(repo["name"], lang, size) for lang, size in repo["languages"].items()],
            )
            db.executemany(
                "INSERT INTO commits VALUES (?, ?, ?)",
                [(c["sha"], repo["name"], c["date"]) for c in repo["commits"]],
            )
    return db


def compute(snapshot: dict) -> Metrics:
    db = load(snapshot)
    try:
        totals = db.execute(_sql("totals")).fetchone()
        return Metrics(
            commits=totals["commits"],
            active_days=totals["active_days"],
            repositories=totals["repositories"],
            first_commit=totals["first_commit"],
            last_commit=totals["last_commit"],
            longest_streak=db.execute(_sql("longest_streak")).fetchone()["longest_streak"],
            daily={r["day"]: r["commits"] for r in db.execute(_sql("daily_commits"))},
            languages=[(r["language"], r["share"]) for r in db.execute(_sql("language_share"))],
        )
    finally:
        db.close()
