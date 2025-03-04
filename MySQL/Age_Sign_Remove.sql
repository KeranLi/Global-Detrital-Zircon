UPDATE `global_u-pb`
SET 
    `Published 206Pb/238U age (Ma)` = CAST(SUBSTRING_INDEX(`Published 206Pb/238U age (Ma)`, '±', 1) AS DOUBLE),
    `Published 206Pb/238U 1σ uncert.` = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 206Pb/238U age (Ma)`, '±', -1), ' ', 1) AS DOUBLE),
    `Published 206Pb/238U 2σ uncert.` = 2 * CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 206Pb/238U age (Ma)`, '±', -1), ' ', 1) AS DOUBLE),
    
    `Published 207Pb/235U age (Ma)` = CAST(SUBSTRING_INDEX(`Published 207Pb/235U age (Ma)`, '±', 1) AS DOUBLE),
    `Published 207Pb/235U 1σ uncert.` = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 207Pb/235U age (Ma)`, '±', -1), ' ', 1) AS DOUBLE),
    `Published 207Pb/235U 2σ uncert.` = 2 * CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 207Pb/235U age (Ma)`, '±', -1), ' ', 1) AS DOUBLE),
    
    `Published 207Pb/206Pb age (Ma)` = CAST(SUBSTRING_INDEX(`Published 207Pb/206Pb age (Ma)`, '±', 1) AS DOUBLE),
    `Published 207Pb/206Pb 1σ uncert.` = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 207Pb/206Pb age (Ma)`, '±', -1), ' ', 1) AS DOUBLE),
    `Published 207Pb/206Pb 2σ uncert.` = 2 * CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(`Published 207Pb/206Pb age (Ma)`, '±', -1), ' ', 1) AS DOUBLE);
