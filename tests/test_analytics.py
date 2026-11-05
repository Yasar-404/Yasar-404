import sqlite3

import pytest

from studio.analytics import compute, load


def snapshot(**commits_by_repo):
    return {
        "user": "someone",
        "repositories": [
            {
                "name": name,
                "description": None,
                "homepage": None,
                "pushed_at": "2026-01-01T00:00:00Z",
                "languages": {"Python": 300, "SQL": 100} if name == "a" else {"Python": 100},
                "commits": [{"sha": f"{name}{i}", "date": day} for i, day in enumerate(days)],
            }
            for name, days in commits_by_repo.items()
        ],
    }


def test_totals_count_days_and_only_repositories_with_commits():
    metrics = compute(snapshot(a=["2026-01-01", "2026-01-01", "2026-01-03"], b=[]))
    assert metrics.commits == 3
    assert metrics.active_days == 2
    assert metrics.repositories == 1
    assert metrics.first_commit == "2026-01-01"
    assert metrics.last_commit == "2026-01-03"
    assert metrics.daily == {"2026-01-01": 2, "2026-01-03": 1}


@pytest.mark.parametrize(
    ("days", "expected"),
    [
        ([], 0),
        (["2026-01-01"], 1),
        (["2026-01-01", "2026-01-03"], 1),
        (["2026-01-31", "2026-02-01", "2026-02-02", "2026-02-10"], 3),
        (["2026-01-01", "2026-01-01", "2026-01-02"], 2),
    ],
)
def test_longest_streak_handles_gaps_duplicates_and_month_ends(days, expected):
    assert compute(snapshot(a=days)).longest_streak == expected


def test_language_shares_sum_to_one_and_sort_by_size():
    metrics = compute(snapshot(a=["2026-01-01"], b=[]))
    assert [name for name, _ in metrics.languages] == ["Python", "SQL"]
    assert metrics.languages[0][1] == pytest.approx(0.8)
    assert sum(share for _, share in metrics.languages) == pytest.approx(1)


def test_schema_rejects_malformed_dates():
    db = load(snapshot(a=[]))
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO commits VALUES ('x', 'a', 'yesterday')")
