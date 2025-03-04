-- UPDATE `global_u-pb` 
-- SET `Best Age` =
-- CASE
-- 	
-- 	WHEN CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) < 1200 THEN
-- 	CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) ELSE CAST( `Published 207Pb/206Pb age (Ma)` AS DOUBLE ) 
-- END;

-- SELECT 
--     SUM(CASE WHEN `Best Age` IS NOT NULL THEN 1 ELSE 0 END) AS Rows_With_Best_Age,
--     SUM(CASE WHEN `Best Age` IS NULL THEN 1 ELSE 0 END) AS Rows_Without_Best_Age
-- FROM `global_u-pb`;

-- SELECT *
-- FROM `global_u-pb`
-- WHERE `Best Age` IS NULL
-- LIMIT 10;

SELECT *
FROM `global_u-pb`
WHERE `Best Age` IS NULL;