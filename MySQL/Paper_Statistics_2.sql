-- SELECT COUNT(DISTINCT `Lead_Author`) AS Unique_Authors
-- FROM `global_u-pb`

-- SELECT COUNT(DISTINCT `Title`) AS Unique_Title
-- FROM `china_u-pb`

-- SELECT COUNT(DISTINCT `Ref_number`) AS Unique_Ref
-- FROM `wu_2023`
-- WHERE Lithology = 'sedimentary';

SELECT DISTINCT `Ref_number`
FROM `wu_2023`
WHERE Lithology = 'sedimentary';
