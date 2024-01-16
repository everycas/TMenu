
SELECT
    m.[SIFR],
    m.[CODE],
    c.[NAME] AS CATEGLIST_NAME,
    m.[NAME] AS MENUITEMS_NAME,
    m.[COMMENT],
    p.[VALUE]
FROM
    [RK7_KATS].[dbo].[MENUITEMS] m
JOIN
    [RK7_KATS].[dbo].[CATEGLIST] c ON m.[PARENT] = c.[SIFR]
JOIN
    [RK7_KATS].[dbo].[PRICES] p ON m.[SIFR] = p.[OBJECTID]
WHERE
    p.[VALUE] IS NOT NULL AND
    p.[VALUE] > 0 AND
    m.[STATUS] = 3;
