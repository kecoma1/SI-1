DROP FUNCTION gettopventas(integer,integer);

CREATE OR REPLACE FUNCTION getTopVentas (year_1 INTEGER, year_2 INTEGER) 
RETURNS TABLE (
ANO		DOUBLE PRECISION,
PELICULA	VARCHAR,
VENTAS		NUMERIC
)
AS $$

DECLARE
i integer:= 0;

BEGIN

	RETURN QUERY
		-- Una vez numeradas las filas solo cogemos la fila numero 1
		SELECT t2.Oano2 AS ANO, b.movietitle AS TITULO, t2.sumadecantidades2 AS VENTAS
		
		FROM	(
			-- Enumeramos cada fila pero agrupandolas por año
			SELECT t1.sumadecantidades1 AS sumadecantidades2, t1.Oano1 AS Oano2, t1.IMDB_Mid1 AS IMDB_Mid2,
			ROW_NUMBER() OVER(PARTITION BY t1.Oano1 ORDER BY t1.sumadecantidades1 DESC) AS rk
			FROM	(
				-- Sumamos las versiones de las peliculas
				SELECT SUM(t0.sumadecantidades) AS sumadecantidades1, t0.Oano0 as Oano1, t0.IMDB_Mid0 AS IMDB_Mid1
				FROM	(
					-- Sumanmos las cantidades de los orderdetails y las separamos por año
					SELECT SUM(t.cantidad) AS sumadecantidades, t.ODp_id AS ODp_id2, t.Oano as Oano0, t.IMDB_Mid AS IMDB_Mid0
					FROM 	(
						-- Seleccionamos todos los orderdetails y los orders con los años
						SELECT d.movieid AS IMDB_Mid, c.prod_id AS Pid, b.orderid AS ODoid, b.prod_id AS ODp_id, b.quantity AS cantidad, EXTRACT(YEAR FROM a.orderdate) AS Oano
						FROM orders AS a, orderdetail AS b, products AS c, imdb_movies as d
						WHERE a.orderid = b.orderid AND ( CAST(EXTRACT(YEAR FROM a.orderdate) AS INTEGER) BETWEEN year_1 AND year_2 )
							AND d.movieid = c.movieid AND c.prod_id = b.prod_id
						) AS t
					GROUP BY ODp_id2, Oano0, IMDB_Mid0
					ORDER BY sumadecantidades DESC
					) AS t0
				GROUP BY Oano1, IMDB_Mid1
				) AS t1, imdb_movies AS c
			GROUP BY Oano2, IMDB_Mid2, sumadecantidades2
			) AS t2, imdb_movies AS b
		-- Seleccionamos solo la primera
		WHERE rk = 1 AND b.movieid = t2.IMDB_Mid2
		ORDER BY VENTAS DESC;

END; $$

LANGUAGE 'plpgsql';

SELECT * FROM getTopVentas(2018, 2020)
