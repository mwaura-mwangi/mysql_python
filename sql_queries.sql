-- create or clone table from existing one
CREATE TABLE coffee_sales_parkroad_two AS
(
 SELECT * FROM coffee_sales_parkroad
);

-- cofee that costs less the 30dollars
SELECT *
FROM coffee_sales_parkroad as c
WHERE money <= 30.00
LIMIT 10;


SELECT sale_date, cash_type, money
FROM coffee_sales_parkroad_two

SELECT SUM(money)
FROM coffee_sales_parkroad_two

SELECT MIN(money)
FROM coffee_sales_parkroad_two

SELECT MAX(money)
FROM coffee_sales_parkroad_two

SELECT AVG(money)
FROM coffee_sales_parkroad_two

SELECT cash_type,
    COUNT(*) AS total_occurences
FROM coffee_sales_parkroad_two
GROUP BY cash_type;

SELECT DISTINCT coffee_name
FROM coffee_sales_parkroad_two

SELECT *
FROM coffee_sales_parkroad_two
ORDER BY sale_datetime DESC

SELECT cash_type
FROM coffee_sales_parkroad_two
WHERE cash_type = 'card'
LIMIT 10;