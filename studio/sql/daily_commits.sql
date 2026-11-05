SELECT committed_on AS day, COUNT(*) AS commits
FROM commits
GROUP BY committed_on
ORDER BY committed_on;
