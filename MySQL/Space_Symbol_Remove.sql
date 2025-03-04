-- SELECT *
-- FROM `global_u-pb`
-- WHERE `Th/U` LIKE '%\r%';

SELECT *
FROM `global_u-pb`
WHERE `Th/U` REGEXP '[^0-9\.\-]';
-
# 0 .05 -> 0.05
-- UPDATE `global_u-pb`
-- SET `Th_ppm` = REPLACE(`Th_ppm`, ' .', '.');

# 0. 05 -> 0.05
-- UPDATE `global_u-pb`
-- SET `U_ppm` = REPLACE(`U_ppm`, '. ', '.');

# 0.05  -> 0.05
-- UPDATE `global_u-pb`
-- SET `Th_ppm` = TRIM(REPLACE(`Th_ppm`, '. ', '.'));

# Delete “NaN” and "no value"
-- DELETE FROM `global_u-pb`
-- WHERE `U_ppm` IN ('NaN', 'no value');
