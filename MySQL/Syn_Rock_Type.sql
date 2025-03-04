SELECT
	COUNT( * ) AS total_rows,-- Sequence: Type 1, Type 2, Type 3
	SUM( COALESCE ( `Class-1 Rock Type`, `Class-2 Rock Type`, `Class-3 Rock Type` ) IS NOT NULL ) AS total_synthetic_1_2_3,
	SUM( COALESCE ( `Class-1 Rock Type`, `Class-2 Rock Type`, `Class-3 Rock Type` ) IS NOT NULL ) / COUNT( * ) AS ratio_synthetic_1_2_3,
	SUM( COALESCE ( `Class-1 Rock Type`, `Class-2 Rock Type`, `Class-3 Rock Type` ) = `Class-1 Rock Type` ) / SUM( COALESCE ( `Class-1 Rock Type`, `Class-2 Rock Type`, `Class-3 Rock Type` ) IS NOT NULL ) AS ratio_type_1_1_2_3,
	SUM( COALESCE ( `Class-1 Rock Type`, `Class-2 Rock Type`, `Class-3 Rock Type` ) = `Class-2 Rock Type` ) / SUM( COALESCE ( `Class-1 Rock Type`, `Class-2 Rock Type`, `Class-3 Rock Type` ) IS NOT NULL ) AS ratio_type_2_1_2_3,
	SUM( COALESCE ( `Class-1 Rock Type`, `Class-2 Rock Type`, `Class-3 Rock Type` ) = `Class-3 Rock Type` ) / SUM( COALESCE ( `Class-1 Rock Type`, `Class-2 Rock Type`, `Class-3 Rock Type` ) IS NOT NULL ) AS ratio_type_3_1_2_3,-- Sequence: Type 2, Type 3, Type 1
	SUM( COALESCE ( `Class-2 Rock Type`, `Class-3 Rock Type`, `Class-1 Rock Type` ) IS NOT NULL ) AS total_synthetic_2_3_1,
	SUM( COALESCE ( `Class-2 Rock Type`, `Class-3 Rock Type`, `Class-1 Rock Type` ) IS NOT NULL ) / COUNT( * ) AS ratio_synthetic_2_3_1,
	SUM( COALESCE ( `Class-2 Rock Type`, `Class-3 Rock Type`, `Class-1 Rock Type` ) = `Class-2 Rock Type` ) / SUM( COALESCE ( `Class-2 Rock Type`, `Class-3 Rock Type`, `Class-1 Rock Type` ) IS NOT NULL ) AS ratio_type_2_2_3_1,
	SUM( COALESCE ( `Class-2 Rock Type`, `Class-3 Rock Type`, `Class-1 Rock Type` ) = `Class-3 Rock Type` ) / SUM( COALESCE ( `Class-2 Rock Type`, `Class-3 Rock Type`, `Class-1 Rock Type` ) IS NOT NULL ) AS ratio_type_3_2_3_1,
	SUM( COALESCE ( `Class-2 Rock Type`, `Class-3 Rock Type`, `Class-1 Rock Type` ) = `Class-1 Rock Type` ) / SUM( COALESCE ( `Class-2 Rock Type`, `Class-3 Rock Type`, `Class-1 Rock Type` ) IS NOT NULL ) AS ratio_type_1_2_3_1,-- Sequence: Type 2, Type 1, Type 3
	SUM( COALESCE ( `Class-2 Rock Type`, `Class-1 Rock Type`, `Class-3 Rock Type` ) IS NOT NULL ) AS total_synthetic_2_1_3,
	SUM( COALESCE ( `Class-2 Rock Type`, `Class-1 Rock Type`, `Class-3 Rock Type` ) IS NOT NULL ) / COUNT( * ) AS ratio_synthetic_2_1_3,
	SUM( COALESCE ( `Class-2 Rock Type`, `Class-1 Rock Type`, `Class-3 Rock Type` ) = `Class-2 Rock Type` ) / SUM( COALESCE ( `Class-2 Rock Type`, `Class-1 Rock Type`, `Class-3 Rock Type` ) IS NOT NULL ) AS ratio_type_2_2_1_3,
	SUM( COALESCE ( `Class-2 Rock Type`, `Class-1 Rock Type`, `Class-3 Rock Type` ) = `Class-1 Rock Type` ) / SUM( COALESCE ( `Class-2 Rock Type`, `Class-1 Rock Type`, `Class-3 Rock Type` ) IS NOT NULL ) AS ratio_type_1_2_1_3,
	SUM( COALESCE ( `Class-2 Rock Type`, `Class-1 Rock Type`, `Class-3 Rock Type` ) = `Class-3 Rock Type` ) / SUM( COALESCE ( `Class-2 Rock Type`, `Class-1 Rock Type`, `Class-3 Rock Type` ) IS NOT NULL ) AS ratio_type_3_2_1_3,-- Sequence: Type 3, Type 1, Type 2
	SUM( COALESCE ( `Class-3 Rock Type`, `Class-1 Rock Type`, `Class-2 Rock Type` ) IS NOT NULL ) AS total_synthetic_3_1_2,
	SUM( COALESCE ( `Class-3 Rock Type`, `Class-1 Rock Type`, `Class-2 Rock Type` ) IS NOT NULL ) / COUNT( * ) AS ratio_synthetic_3_1_2,
	SUM( COALESCE ( `Class-3 Rock Type`, `Class-1 Rock Type`, `Class-2 Rock Type` ) = `Class-3 Rock Type` ) / SUM( COALESCE ( `Class-3 Rock Type`, `Class-1 Rock Type`, `Class-2 Rock Type` ) IS NOT NULL ) AS ratio_type_3_3_1_2,
	SUM( COALESCE ( `Class-3 Rock Type`, `Class-1 Rock Type`, `Class-2 Rock Type` ) = `Class-1 Rock Type` ) / SUM( COALESCE ( `Class-3 Rock Type`, `Class-1 Rock Type`, `Class-2 Rock Type` ) IS NOT NULL ) AS ratio_type_1_3_1_2,
	SUM( COALESCE ( `Class-3 Rock Type`, `Class-1 Rock Type`, `Class-2 Rock Type` ) = `Class-2 Rock Type` ) / SUM( COALESCE ( `Class-3 Rock Type`, `Class-1 Rock Type`, `Class-2 Rock Type` ) IS NOT NULL ) AS ratio_type_2_3_1_2,-- Sequence: Type 3, Type 2, Type 1
	SUM( COALESCE ( `Class-3 Rock Type`, `Class-2 Rock Type`, `Class-1 Rock Type` ) IS NOT NULL ) AS total_synthetic_3_2_1,
	SUM( COALESCE ( `Class-3 Rock Type`, `Class-2 Rock Type`, `Class-1 Rock Type` ) IS NOT NULL ) / COUNT( * ) AS ratio_synthetic_3_2_1,
	SUM( COALESCE ( `Class-3 Rock Type`, `Class-2 Rock Type`, `Class-1 Rock Type` ) = `Class-3 Rock Type` ) / SUM( COALESCE ( `Class-3 Rock Type`, `Class-2 Rock Type`, `Class-1 Rock Type` ) IS NOT NULL ) AS ratio_type_3_3_2_1,
	SUM( COALESCE ( `Class-3 Rock Type`, `Class-2 Rock Type`, `Class-1 Rock Type` ) = `Class-2 Rock Type` ) / SUM( COALESCE ( `Class-3 Rock Type`, `Class-2 Rock Type`, `Class-1 Rock Type` ) IS NOT NULL ) AS ratio_type_2_3_2_1,
	SUM( COALESCE ( `Class-3 Rock Type`, `Class-2 Rock Type`, `Class-1 Rock Type` ) = `Class-1 Rock Type` ) / SUM( COALESCE ( `Class-3 Rock Type`, `Class-2 Rock Type`, `Class-1 Rock Type` ) IS NOT NULL ) AS ratio_type_1_3_2_1,-- Sequence: Type 1, Type 3, Type 2
	SUM( COALESCE ( `Class-1 Rock Type`, `Class-3 Rock Type`, `Class-2 Rock Type` ) IS NOT NULL ) AS total_synthetic_1_3_2,
	SUM( COALESCE ( `Class-1 Rock Type`, `Class-3 Rock Type`, `Class-2 Rock Type` ) IS NOT NULL ) / COUNT( * ) AS ratio_synthetic_1_3_2,
	SUM( COALESCE ( `Class-1 Rock Type`, `Class-3 Rock Type`, `Class-2 Rock Type` ) = `Class-1 Rock Type` ) / SUM( COALESCE ( `Class-1 Rock Type`, `Class-3 Rock Type`, `Class-2 Rock Type` ) IS NOT NULL ) AS ratio_type_1_1_3_2,
	SUM( COALESCE ( `Class-1 Rock Type`, `Class-3 Rock Type`, `Class-2 Rock Type` ) = `Class-3 Rock Type` ) / SUM( COALESCE ( `Class-1 Rock Type`, `Class-3 Rock Type`, `Class-2 Rock Type` ) IS NOT NULL ) AS ratio_type_3_1_3_2,
	SUM( COALESCE ( `Class-1 Rock Type`, `Class-3 Rock Type`, `Class-2 Rock Type` ) = `Class-2 Rock Type` ) / SUM( COALESCE ( `Class-1 Rock Type`, `Class-3 Rock Type`, `Class-2 Rock Type` ) IS NOT NULL ) AS ratio_type_2_1_3_2 
FROM
	`global_u-pb`;