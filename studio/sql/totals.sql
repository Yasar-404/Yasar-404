SELECT
    COUNT(*)                     AS commits,
    COUNT(DISTINCT committed_on) AS active_days,
    COUNT(DISTINCT repository)   AS repositories,
    MIN(committed_on)            AS first_commit,
    MAX(committed_on)            AS last_commit
FROM commits;
