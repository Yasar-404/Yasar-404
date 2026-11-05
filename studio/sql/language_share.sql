SELECT
    language,
    SUM(bytes)                                 AS bytes,
    1.0 * SUM(bytes) / SUM(SUM(bytes)) OVER () AS share
FROM language_bytes
GROUP BY language
ORDER BY bytes DESC, language;
