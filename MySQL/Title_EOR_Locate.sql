UPDATE `global_u-pb`
SET `Title` = REPLACE(`Title`, '\'', '\'\'')
WHERE `Title` LIKE '%\'%';

-- UPDATE `global_u-pb`
-- SET `Title` = REPLACE(`Title`, '\'', '\'\'')
-- WHERE `Title` LIKE '%\'%';

-- SELECT * FROM `global_u-pb`
-- WHERE `Title` LIKE '%\'%';

-- UPDATE `global_u-pb`
-- SET `Title` = REPLACE(REPLACE(`Title`, 'Lu?Hf', 'Lu-Hf'), 'Meta?Sedimentary', 'Meta-Sedimentary')
-- WHERE `Title` LIKE '%Lu?Hf%' OR `Title` LIKE '%Meta?Sedimentary%';
