-- Normalised view of a GitHub account. Rebuilt from data/snapshot.json on each run.
CREATE TABLE repositories (
    name        TEXT PRIMARY KEY,
    description TEXT,
    homepage    TEXT,
    pushed_at   TEXT NOT NULL
) STRICT;

CREATE TABLE language_bytes (
    repository TEXT    NOT NULL REFERENCES repositories (name),
    language   TEXT    NOT NULL,
    bytes      INTEGER NOT NULL CHECK (bytes >= 0),
    PRIMARY KEY (repository, language)
) STRICT;

CREATE TABLE commits (
    sha          TEXT PRIMARY KEY,
    repository   TEXT NOT NULL REFERENCES repositories (name),
    committed_on TEXT NOT NULL CHECK (committed_on GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]')
) STRICT;

CREATE INDEX commits_by_day ON commits (committed_on);
