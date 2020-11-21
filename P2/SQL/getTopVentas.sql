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
	-- De los años establecidos, coger la pelicula 1 de cada año y hacer print de mayor a menor
	SELECT t.ano, t.titulo as pelicula, MAX(t.max_sales) as ventas
		FROM 	(	
			-- Obtenemos las ventas de cada año y las enumeramos de mayor a menor (la que más ventas tiene es la 1) 
			SELECT a.year as ano, MAX(c.sales) as max_sales, a.movietitle as titulo,

			-- Una por año, enumeramos cada película por año
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
