"""Real public activity, computed in SQL from the GitHub API and rebuilt every night."""

from __future__ import annotations

from datetime import date, timedelta

from ..analytics import Metrics
from ..svg import EASE, MARGIN, WIDTH, Doc
from ..theme import Theme

HEIGHT = 330
WEEKS = 26
CELL, GAP = 14, 3
MAX_LANGUAGES = 5
MEANINGFUL_STREAK = 7


def heat_level(commits: int) -> int:
    if commits <= 0:
        return 0
    if commits == 1:
        return 1
    if commits == 2:
        return 2
    return 3 if commits <= 4 else 4


def _heatmap(doc: Doc, metrics: Metrics, x0: float, y0: float) -> str:
    """Weeks run left to right and end on the latest commit, so output is deterministic."""
    t = doc.theme
    end = date.fromisoformat(metrics.last_commit) if metrics.last_commit else date(2026, 1, 1)
    week_start = end - timedelta(days=(end.weekday() + 1) % 7)
    first = week_start - timedelta(weeks=WEEKS - 1)
    cells = []
    for w in range(WEEKS):
        for d in range(7):
            day = first + timedelta(weeks=w, days=d)
            if day > end:
                continue
            count = metrics.daily.get(day.isoformat(), 0)
            level = heat_level(count)
            cls = ' class="beat"' if level else ""
            delay = f' style="animation-delay:{w * 0.12:.2f}s"' if level else ""
            cells.append(
                f'<rect{cls}{delay} x="{x0 + w * (CELL + GAP)}" y="{y0 + d * (CELL + GAP)}" '
                f'width="{CELL}" height="{CELL}" rx="3" fill="{t.heat[level]}"/>'
            )
    return "".join(cells)


def render(theme: Theme, metrics: Metrics) -> str:
    languages = ", ".join(
        f"{name} {share:.0%}" for name, share in metrics.languages[:MAX_LANGUAGES]
    )
    doc = Doc(
        theme,
        f"Public GitHub activity: {metrics.commits} commits across {metrics.repositories} "
        f"repositories, {metrics.active_days} active days, longest streak "
        f"{metrics.longest_streak} days. Languages: {languages}",
        HEIGHT,
    )
    t = theme
    doc.style(
        f".beat{{animation:beat 6s {EASE} infinite}}"
        "@keyframes beat{0%,12%,100%{opacity:1}6%{opacity:.45}}"
        f".lang{{transform-box:fill-box;transform-origin:left;animation:lang 8s {EASE} infinite}}"
        "@keyframes lang{0%{transform:scaleX(.03)}18%,90%{transform:scaleX(1)}"
        "100%{transform:scaleX(.03)}}",
        ".beat,.lang{animation:none}",
    )
    doc.add(
        doc.section_header("05", "LIVE FROM THE GITHUB API", "PYTHON + SQLITE, REBUILT NIGHTLY")
    )

    # A streak only says something once it is long enough to be a habit.
    fourth = (
        (str(metrics.longest_streak), "LONGEST STREAK, DAYS")
        if metrics.longest_streak >= MEANINGFUL_STREAK
        else (str(len(metrics.languages)), "LANGUAGES")
    )
    stats = (
        (str(metrics.commits), "PUBLIC COMMITS"),
        (str(metrics.repositories), "ACTIVE REPOSITORIES"),
        (str(metrics.active_days), "ACTIVE DAYS"),
        fourth,
    )
    cell = (WIDTH - 2 * MARGIN) / len(stats)
    for i, (value, label) in enumerate(stats):
        x = MARGIN + i * cell
        doc.add(
            doc.text(x, 106, value, "sans", 300, 42, "ink", track=-1),
            doc.label_text(x, 128, label, "faint", size=10, track=1.5),
        )

    grid_y = 164
    doc.add(
        doc.label_text(
            MARGIN, grid_y - 10, f"LAST {WEEKS} WEEKS OF COMMITS", "muted", size=10.5, track=1.8
        ),
        _heatmap(doc, metrics, MARGIN, grid_y),
    )

    bars_x = MARGIN + WEEKS * (CELL + GAP) + 52
    name_w = 84
    track_x = bars_x + name_w
    track_w = WIDTH - MARGIN - track_x - 44
    doc.add(
        doc.label_text(bars_x, grid_y - 10, "LANGUAGES BY BYTES", "muted", size=10.5, track=1.8)
    )
    top = metrics.languages[0][1] if metrics.languages else 1
    for i, (name, share) in enumerate(metrics.languages[:MAX_LANGUAGES]):
        y = grid_y + 3 + i * 23
        doc.add(
            doc.text(bars_x, y + 9, name, "sans", 500, 12.5, "ink"),
            f'<rect class="lang" x="{track_x}" y="{y}" width="{share / top * track_w:.1f}" '
            f'height="10" rx="3" fill="{t.accent}"/>',
            doc.text(WIDTH - MARGIN, y + 9, f"{share:.0%}", "mono", 400, 11.5, "muted", "end"),
        )
    return doc.render()
