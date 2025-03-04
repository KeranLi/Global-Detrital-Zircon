SELECT
	`Journal`,
	COUNT( DISTINCT `Title` ) AS Paper_Count,
	GROUP_CONCAT( DISTINCT `Title` SEPARATOR '; ' ) AS Paper_Titles 
FROM
	`global_u-pb` 
GROUP BY
	`Journal` 
ORDER BY
	Paper_Count DESC;