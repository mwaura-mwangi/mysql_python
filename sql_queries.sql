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


SELECT *
FROM coffee_sales_parkroad_two
