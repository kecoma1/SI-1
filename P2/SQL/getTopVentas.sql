DROP FUNCTION getTopVentas (year_1 INTEGER, year_2 INTEGER);

CREATE OR REPLACE FUNCTION getTopVentas (year_1 INTEGER, year_2 INTEGER) 
RETURNS TABLE (
ANO		TEXT,
VENTAS		INTEGER,
PELICULA	VARCHAR
)
AS $$

DECLARE
i integer:= 0;

BEGIN

IF (year_1 < year_2) then
	i := year_1;
ELSE
	i := year_2;
END IF;

WHILE i<=year_2 LOOP
	RETURN QUERY
	SELECT a.year as ano, MAX(c.sales) as max_sales, a.movietitle as titulo
			FROM imdb_movies as a, products as b, inventory as c
			WHERE a.movieid = b.movieid AND c.prod_id = b.prod_id AND CAST(a.year AS INT) = i
			GROUP BY a.year, a.movietitle
			ORDER BY max_sales DESC
			LIMIT 1;
	i:= i+1;
END LOOP;

END; $$

LANGUAGE 'plpgsql';

SELECT * FROM getTopVentas(1995, 2000) as v ORDER BY v.ventas DESC

