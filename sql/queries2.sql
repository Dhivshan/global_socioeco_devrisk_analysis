# Analysis

# Average income per segment
SELECT Segment, AVG(income) AS avg_income FROM country_stats GROUP BY Segment ORDER BY avg_income DESC;

# Top 10 high-risk countries

SELECT country FROM country_stats WHERE Segment='High Risk Country' ORDER BY country LIMIT 10;

# Countries with highest inflation
SELECT country, inflation FROM country_stats ORDER BY inflation DESC LIMIT 10;

# Countries with lowest GDP per capita
SELECT country, gdpp FROM country_stats ORDER BY gdpp ASC LIMIT 10;

# Average life expectancy by segment
SELECT Segment, AVG(life_expec) AS avg_life_expec FROM country_stats GROUP BY Segment ORDER BY avg_life_expec;

# Fertility rate comparison across Segments
SELECT Segment, AVG(total_fer) AS avg_fertility_rate,
 CASE 
	WHEN AVG(total_fer) >= 4 THEN 'High Fertility'
	WHEN AVG(total_fer) BETWEEN 2 AND 4 THEN 'Moderate Fertility'
	ELSE 'Low Fertility'
	END AS fertility_category
FROM country_stats
GROUP BY Segment
ORDER BY avg_fertility_rate DESC;


