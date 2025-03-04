-- SELECT *
-- FROM `global_u-pb`
-- WHERE `Published 206Pb/238U age (Ma)` REGEXP '[^0-9.±-]' 
--    OR `Published 207Pb/235U age (Ma)` REGEXP '[^0-9.±-]' 
--    OR `Published 207Pb/206Pb age (Ma)` REGEXP '[^0-9.±-]';

-- SELECT *
-- FROM `global_u-pb`
-- WHERE `Published 206Pb/238U age (Ma)` LIKE '%?%'
--    OR `Published 207Pb/235U age (Ma)` LIKE '%?%'
--    OR `Published 207Pb/206Pb age (Ma)` LIKE '%?%';

UPDATE `global_u-pb`
SET 
    `Published 206Pb/238U age (Ma)` = CAST(REGEXP_REPLACE(SUBSTRING_INDEX(`Published 206Pb/238U age (Ma)`, '±', 1), '[^0-9.]', '') AS DOUBLE),
    `Published 206Pb/238U 1σ uncert.` = CAST(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 206Pb/238U age (Ma)`, '±', -1), ' ', 1), '[^0-9.]', '') AS DOUBLE),
    `Published 206Pb/238U 2σ uncert.` = 2 * CAST(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 206Pb/238U age (Ma)`, '±', -1), ' ', 1), '[^0-9.]', '') AS DOUBLE),
    
    `Published 207Pb/235U age (Ma)` = CAST(REGEXP_REPLACE(SUBSTRING_INDEX(`Published 207Pb/235U age (Ma)`, '±', 1), '[^0-9.]', '') AS DOUBLE),
    `Published 207Pb/235U 1σ uncert.` = CAST(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 207Pb/235U age (Ma)`, '±', -1), ' ', 1), '[^0-9.]', '') AS DOUBLE),
    `Published 207Pb/235U 2σ uncert.` = 2 * CAST(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 207Pb/235U age (Ma)`, '±', -1), ' ', 1), '[^0-9.]', '') AS DOUBLE),
    
    `Published 207Pb/206Pb age (Ma)` = CAST(REGEXP_REPLACE(SUBSTRING_INDEX(`Published 207Pb/206Pb age (Ma)`, '±', 1), '[^0-9.]', '') AS DOUBLE),
    `Published 207Pb/206Pb 1σ uncert.` = CAST(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 207Pb/206Pb age (Ma)`, '±', -1), ' ', 1), '[^0-9.]', '') AS DOUBLE),
    `Published 207Pb/206Pb 2σ uncert.` = 2 * CAST(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 207Pb/206Pb age (Ma)`, '±', -1), ' ', 1), '[^0-9.]', '') AS DOUBLE);
