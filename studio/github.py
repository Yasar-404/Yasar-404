"""Fetch a public snapshot of a GitHub account through the REST API."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from collections.abc import Iterator
from pathlib import Path

API = "https://api.github.com"


class GitHubError(RuntimeError):
    pass


class GitHubClient:
    def __init__(self, token: str | None = None) -> None:
        self.token = token if token is not None else os.environ.get("GITHUB_TOKEN")

    def _request(self, url: str) -> tuple[object, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "profile-studio",
        }
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response), response.headers.get("Link", "")

    def get(self, path: str) -> object:
        try:
            return self._request(f"{API}{path}")[0]
        except urllib.error.HTTPError as err:
            raise GitHubError(f"GET {path}: HTTP {err.code}") from err

    def paginate(self, path: str) -> Iterator[dict]:
        url: str | None = f"{API}{path}"
        while url:
            try:
                page, link = self._request(url)
            except urllib.error.HTTPError as err:
                if err.code == 409:  # An empty repository has no commits to list.
                    return
                raise GitHubError(f"GET {url}: HTTP {err.code}") from err
            yield from page
            url = next_page(link)


def next_page(link_header: str) -> str | None:
    for part in link_header.split(","):
        target, _, rel = part.partition(";")
        if 'rel="next"' in rel:
            return target.strip().strip("<>")
    return None


def is_automated(commit: dict) -> bool:
    author = commit.get("author") or {}
    return author.get("type") == "Bot" or author.get("login", "").endswith("[bot]")


def fetch_snapshot(user: str, client: GitHubClient | None = None) -> dict:
    """Return every public, non-fork repository with its languages and human commits."""
    client = client or GitHubClient()
    repositories = []
    for repo in client.paginate(f"/users/{user}/repos?per_page=100&type=owner&sort=full_name"):
        if repo["fork"]:
            continue
        name = repo["name"]
        commits = [
            {"sha": c["sha"], "date": c["commit"]["author"]["date"][:10]}
            for c in client.paginate(f"/repos/{user}/{name}/commits?per_page=100")
            if not is_automated(c)
        ]
        repositories.append(
            {
                "name": name,
                "description": repo["description"],
                "homepage": repo["homepage"],
                "pushed_at": repo["pushed_at"],
                "languages": client.get(f"/repos/{user}/{name}/languages"),
                "commits": commits,
            }
        )
    return {"user": user, "repositories": repositories}


def save_snapshot(snapshot: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_snapshot(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))
