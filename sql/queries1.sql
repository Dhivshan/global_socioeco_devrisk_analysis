CREATE DATABASE global_socioeco_devrisk;
USE global_socioeco_devrisk;

SELECT * FROM country_stats;


# Rule Based Country Segmentation and Risk_Flag based on Segmentation logic

SELECT country,
CASE
    WHEN child_mort > 80 AND income < 5000 THEN 'High Risk Country'
    WHEN income > 30000 AND life_expec > 78 THEN 'Developed Nation'
    WHEN income BETWEEN 8000 AND 30000 THEN 'Emerging Economy'
    WHEN inflation > 15 THEN 'High Inflation Risk'
    WHEN health < 5 AND child_mort > 70 THEN 'Health Critical'
    WHEN gdpp < 2000 THEN 'Low GDP Trap'
    ELSE 'Other'
END AS Segment,
CASE
    WHEN child_mort > 80 AND income < 5000 THEN 1
    WHEN inflation > 15 THEN 1
    WHEN health < 5 AND child_mort > 70 THEN 1
    WHEN gdpp < 2000 THEN 1
    ELSE 0
END AS Risk_Flag
FROM country_stats;