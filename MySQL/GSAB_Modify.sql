-- Update the Journal column to remove volume information
UPDATE `global_u-pb`
SET `Journal` = 'Geological Society of America Bulletin'
WHERE `Journal` LIKE 'Geological Society of America Bulletin, v.%';

-- Extract and set the Volume information in the Volume column
UPDATE `global_u-pb`
SET `Vol.` = TRIM(REPLACE(SUBSTRING_INDEX(`Journal`, 'v. ', -1), ',', ''))
WHERE `Journal` LIKE 'Geological Society of America Bulletin, v.%';

