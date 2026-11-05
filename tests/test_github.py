import io
import urllib.error

from studio.github import GitHubClient, fetch_snapshot, is_automated, next_page


def test_next_page_reads_link_header():
    header = '<https://api.x/a?page=2>; rel="next", <https://api.x/a?page=9>; rel="last"'
    assert next_page(header) == "https://api.x/a?page=2"
    assert next_page('<https://api.x/a?page=1>; rel="prev"') is None
    assert next_page("") is None


def test_is_automated():
    assert is_automated({"author": {"login": "github-actions[bot]", "type": "Bot"}})
    assert not is_automated({"author": {"login": "someone", "type": "User"}})
    assert not is_automated({"author": None})


class FakeClient(GitHubClient):
    """Serves canned API pages, including the 409 GitHub returns for an empty repository."""

    def __init__(self, routes):
        super().__init__(token="")
        self.routes = routes

    def _request(self, url):
        for fragment, response in self.routes.items():
            if fragment in url:
                if isinstance(response, int):
                    raise urllib.error.HTTPError(url, response, "", None, io.BytesIO())
                return response, ""
        raise AssertionError(f"unexpected request: {url}")


def commit(sha, date, login="someone", kind="User"):
    return {
        "sha": sha,
        "author": {"login": login, "type": kind},
        "commit": {"author": {"date": f"{date}T10:00:00Z"}},
    }


def repo(name, fork=False):
    return {
        "name": name,
        "fork": fork,
        "description": None,
        "homepage": None,
        "pushed_at": "2026-01-01T00:00:00Z",
    }


def test_snapshot_skips_forks_and_bots_and_survives_empty_repositories():
    client = FakeClient(
        {
            "/users/someone/repos": [repo("app"), repo("empty"), repo("forked", fork=True)],
            "/repos/someone/app/commits": [
                commit("a", "2026-01-02"),
                commit("b", "2026-01-03", "github-actions[bot]", "Bot"),
            ],
            "/repos/someone/app/languages": {"Python": 10},
            "/repos/someone/empty/commits": 409,
            "/repos/someone/empty/languages": {},
        }
    )
    snapshot = fetch_snapshot("someone", client)
    by_name = {r["name"]: r for r in snapshot["repositories"]}
    assert set(by_name) == {"app", "empty"}
    assert by_name["app"]["commits"] == [{"sha": "a", "date": "2026-01-02"}]
    assert by_name["empty"]["commits"] == []
