DROP FUNCTION getTopVentas (year_1 INTEGER, year_2 INTEGER);

CREATE OR REPLACE FUNCTION getTopVentas (year_1 INTEGER, year_2 INTEGER) 
RETURNS TABLE (
ANO		TEXT,
PELICULA	VARCHAR,
VENTAS		INTEGER
)
AS $$

DECLARE
i integer:= 0;

BEGIN

	RETURN QUERY
	SELECT t.ano, t.titulo as pelicula, MAX(t.max_sales) as ventas
		FROM 	(	
			SELECT a.year as ano, MAX(c.sales) as max_sales, a.movietitle as titulo,
			ROW_NUMBER() OVER(PARTITION BY a.year ORDER BY MAX(c.sales) DESC) AS rk
				FROM imdb_movies as a, products as b, inventory as c
				WHERE a.movieid = b.movieid AND c.prod_id = b.prod_id AND CAST(a.year AS INTEGER) BETWEEN year_1 AND year_2
				GROUP BY a.year, a.movietitle
				ORDER BY max_sales DESC
			) as t
WHERE t.rk = 1
GROUP BY t.ano, t.titulo
ORDER BY ventas DESC;

END; $$

LANGUAGE 'plpgsql';

SELECT * FROM getTopVentas(1985, 1990)
