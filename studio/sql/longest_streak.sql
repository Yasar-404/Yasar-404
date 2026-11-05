-- Gaps and islands: consecutive days share the same (day number - row number).
WITH days AS (
    SELECT DISTINCT committed_on AS day FROM commits
),
islands AS (
    SELECT
        day,
        CAST(julianday(day) AS INTEGER) - ROW_NUMBER() OVER (ORDER BY day) AS island
    FROM days
)
SELECT COALESCE(MAX(length), 0) AS longest_streak
FROM (SELECT COUNT(*) AS length FROM islands GROUP BY island);
