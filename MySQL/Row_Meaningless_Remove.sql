DELETE FROM `global_u-pb`
WHERE `Published 206Pb/238U age (Ma)` IS NULL
  AND `Published 207Pb/235U age (Ma)` IS NULL
  AND `Published 207Pb/206Pb age (Ma)` IS NULL
  AND `Best Age` IS NULL;
