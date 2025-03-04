SELECT 
    COUNT(*) AS total_rows,
    SUM(`Class-1 Rock Type` IS NOT NULL AND `Class-2 Rock Type` IS NOT NULL AND `Class-3 Rock Type` IS NOT NULL) AS all_three,
    SUM(`Class-1 Rock Type` IS NOT NULL AND `Class-2 Rock Type` IS NOT NULL AND `Class-3 Rock Type` IS NULL) AS class_1_and_2,
    SUM(`Class-1 Rock Type` IS NOT NULL AND `Class-2 Rock Type` IS NULL AND `Class-3 Rock Type` IS NOT NULL) AS class_1_and_3,
    SUM(`Class-1 Rock Type` IS NULL AND `Class-2 Rock Type` IS NOT NULL AND `Class-3 Rock Type` IS NOT NULL) AS class_2_and_3,
    SUM(`Class-1 Rock Type` IS NOT NULL AND `Class-2 Rock Type` IS NULL AND `Class-3 Rock Type` IS NULL) AS only_class_1,
    SUM(`Class-1 Rock Type` IS NULL AND `Class-2 Rock Type` IS NOT NULL AND `Class-3 Rock Type` IS NULL) AS only_class_2,
    SUM(`Class-1 Rock Type` IS NULL AND `Class-2 Rock Type` IS NULL AND `Class-3 Rock Type` IS NOT NULL) AS only_class_3,
    SUM(`Class-1 Rock Type` IS NULL AND `Class-2 Rock Type` IS NULL AND `Class-3 Rock Type` IS NULL) AS none_of_them,
    SUM(`Class-1 Rock Type` IS NOT NULL AND `Class-2 Rock Type` IS NOT NULL AND `Class-3 Rock Type` IS NOT NULL) / COUNT(*) AS ratio_all_three,
    SUM(`Class-1 Rock Type` IS NOT NULL AND `Class-2 Rock Type` IS NOT NULL AND `Class-3 Rock Type` IS NULL) / COUNT(*) AS ratio_class_1_and_2,
    SUM(`Class-1 Rock Type` IS NOT NULL AND `Class-2 Rock Type` IS NULL AND `Class-3 Rock Type` IS NOT NULL) / COUNT(*) AS ratio_class_1_and_3,
    SUM(`Class-1 Rock Type` IS NULL AND `Class-2 Rock Type` IS NOT NULL AND `Class-3 Rock Type` IS NOT NULL) / COUNT(*) AS ratio_class_2_and_3,
    SUM(`Class-1 Rock Type` IS NOT NULL AND `Class-2 Rock Type` IS NULL AND `Class-3 Rock Type` IS NULL) / COUNT(*) AS ratio_only_class_1,
    SUM(`Class-1 Rock Type` IS NULL AND `Class-2 Rock Type` IS NOT NULL AND `Class-3 Rock Type` IS NULL) / COUNT(*) AS ratio_only_class_2,
    SUM(`Class-1 Rock Type` IS NULL AND `Class-2 Rock Type` IS NULL AND `Class-3 Rock Type` IS NOT NULL) / COUNT(*) AS ratio_only_class_3,
    SUM(`Class-1 Rock Type` IS NULL AND `Class-2 Rock Type` IS NULL AND `Class-3 Rock Type` IS NULL) / COUNT(*) AS ratio_none_of_them
FROM `china_u-pb`;
