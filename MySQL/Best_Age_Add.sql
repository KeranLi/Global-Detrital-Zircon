-- UPDATE `global_u-pb` 
-- SET `Best Age` =
-- CASE
-- 	
-- 	WHEN CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) < 1200 THEN
-- 	CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) 
-- 	WHEN `Published 207Pb/206Pb age (Ma)` IS NOT NULL 
-- 	AND `Published 207Pb/206Pb age (Ma)` <> '' THEN
-- 		CAST( `Published 207Pb/206Pb age (Ma)` AS DOUBLE ) 
-- 		WHEN `Published 207Pb/235U age (Ma)` IS NOT NULL 
-- 		AND `Published 207Pb/235U age (Ma)` <> '' THEN
-- 			CAST( `Published 207Pb/235U age (Ma)` AS DOUBLE ) 
-- 			WHEN `206Pb/238U  isotope ratio` IS NOT NULL 
-- 			AND `206Pb/238U  isotope ratio` <> '' THEN
-- 				( LOG( 1 + CAST( `206Pb/238U  isotope ratio` AS DOUBLE ) ) / 1.55125e-10 ) ELSE CAST( `206Pb/238U  isotope ratio` AS DOUBLE ) -- Fallback to 206Pb/238U age if no other age is available
-- 			
-- END;
-- UPDATE `global_u-pb` 
-- SET `Best Age` = COALESCE (
-- CASE
-- 	
-- 	WHEN CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) < 1200 THEN CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) WHEN CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) >= 1200 
-- 	AND `Published 207Pb/206Pb age (Ma)` IS NOT NULL 
-- 	AND `Published 207Pb/206Pb age (Ma)` <> '' THEN
-- 		CAST( `Published 207Pb/206Pb age (Ma)` AS DOUBLE ) 
-- 		WHEN ( `Published 206Pb/238U age (Ma)` IS NULL OR CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) >= 1200 ) 
-- 		AND `Published 207Pb/235U age (Ma)` IS NOT NULL 
-- 		AND `Published 207Pb/235U age (Ma)` <> '' THEN
-- 			CAST( `Published 207Pb/235U age (Ma)` AS DOUBLE ) ELSE NULL 
-- 		END,
-- 		( LOG( 1 + CAST( `206Pb/238U  isotope ratio` AS DOUBLE ) ) / 1.55125e-10 ),
-- 		CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ),
-- 		CAST( `Published 207Pb/206Pb age (Ma)` AS DOUBLE ),
-- 		CAST( `Published 207Pb/235U age (Ma)` AS DOUBLE ) 
-- 	) 
-- WHERE
-- 	`Best Age` IS NULL 
-- AND ( `Published 206Pb/238U age (Ma)` IS NOT NULL OR `Published 207Pb/206Pb age (Ma)` IS NOT NULL OR `Published 207Pb/235U age (Ma)` IS NOT NULL OR `206Pb/238U  isotope ratio` IS NOT NULL );

UPDATE `global_u-pb` 
SET `Best Age` = COALESCE (
CASE
	
	WHEN CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) < 1200 THEN CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) WHEN CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) >= 1200 
	AND `Published 207Pb/206Pb age (Ma)` IS NOT NULL 
	AND `Published 207Pb/206Pb age (Ma)` <> '' THEN
		CAST( `Published 207Pb/206Pb age (Ma)` AS DOUBLE ) 
		WHEN ( `Published 206Pb/238U age (Ma)` IS NULL OR CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ) >= 1200 ) 
		AND `Published 207Pb/235U age (Ma)` IS NOT NULL 
		AND `Published 207Pb/235U age (Ma)` <> '' THEN
			CAST( `Published 207Pb/235U age (Ma)` AS DOUBLE ) ELSE NULL 
		END,
		( LOG( 1 + CAST( `206Pb/238U  isotope ratio` AS DOUBLE ) ) / 1.55125e-10 ),
		CAST( `Published 206Pb/238U age (Ma)` AS DOUBLE ),
		CAST( `Published 207Pb/206Pb age (Ma)` AS DOUBLE ),
		CAST( `Published 207Pb/235U age (Ma)` AS DOUBLE ),
		GREATEST( CAST( `Best Age uncertainty (±1σ)` AS DOUBLE ), CAST( `Best Age uncertainty (±2σ)` AS DOUBLE ) ),
		COALESCE ( CAST( `Best Age uncertainty (±1σ)` AS DOUBLE ), CAST( `Best Age uncertainty (±2σ)` AS DOUBLE ) ) 
	) 
WHERE
	`Best Age` IS NULL 
	AND (
		`Published 206Pb/238U age (Ma)` IS NOT NULL 
		OR `Published 207Pb/206Pb age (Ma)` IS NOT NULL 
		OR `Published 207Pb/235U age (Ma)` IS NOT NULL 
		OR `206Pb/238U  isotope ratio` IS NOT NULL 
		OR `Best Age uncertainty (±1σ)` IS NOT NULL 
	OR `Best Age uncertainty (±2σ)` IS NOT NULL 
);