SELECT
	`Journal`,
	COUNT( * ) AS Count 
FROM
	`global_lu-hf`
GROUP BY
	`Journal`
ORDER BY
	Count DESC;