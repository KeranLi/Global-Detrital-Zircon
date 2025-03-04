DELETE FROM `global_u-pb`
WHERE `Lead_Author` IS NULL
  AND `Web_Link` IS NULL
  AND `Journal` IS NULL
  AND `Year` IS NULL
  AND `Title` IS NULL;