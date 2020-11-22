CREATE OR REPLACE FUNCTION getTopVentas (year_1 INTEGER, year_2 INTEGER) 
RETURNS TABLE (
ANO		DOUBLE PRECISION,
PELICULA	VARCHAR,
VENTAS		BIGINT
)
AS $$

DECLARE
i integer:= 0;

BEGIN

	RETURN QUERY
		-- Una vez numeradas las filas solo cogemos la fila numero 1
		SELECT t1.ANO0 AS ANO, t1.TITULO0 AS TITULO, t1.sumadecantidades0 AS VENTAS
		FROM
			(
			-- Obtenemos los datos que se nos piden en la query
			-- Enumeramos las filas pero separandolas en años, de mayor a menor con respecto a las ventas, así podremos coger solo una
			SELECT t0.Oano2 AS ANO0, c.movietitle AS TITULO0, MAX(t0.sumadecantidades) AS sumadecantidades0, 
						ROW_NUMBER() OVER(PARTITION BY t0.Oano2 ORDER BY t0.sumadecantidades DESC) AS rk
			FROM	(
				-- Sumanmos las cantidades de los orderdetails y las separamos por año
				SELECT SUM(t.cantidad) AS sumadecantidades, t.ODp_id AS ODp_id2, t.Oano as Oano2
				FROM 	(
					-- Seleccionamos todos los orderdetails y los orders con los años
					SELECT b.orderid AS ODoid, b.prod_id AS ODp_id, b.quantity AS cantidad, EXTRACT(YEAR FROM a.orderdate) AS Oano
					FROM orders AS a, orderdetail AS b
					WHERE a.orderid = b.orderid AND CAST(EXTRACT(YEAR FROM a.orderdate) AS INTEGER) <= 2020 AND CAST(EXTRACT(YEAR FROM a.orderdate) AS INTEGER) >= 2018
					) AS t
				GROUP BY ODp_id2, Oano2
				ORDER BY sumadecantidades DESC
				) AS t0, imdb_movies AS c, products AS d
			WHERE c.movieid = d.movieid AND d.prod_id = t0.ODp_id2
			GROUP BY ANO0, TITULO0, t0.sumadecantidades
			ORDER BY sumadecantidades0 DESC
			) AS t1
		-- Seleccionamos solo la primera
		WHERE t1.rk = 1
		ORDER BY VENTAS DESC;

END; $$

LANGUAGE 'plpgsql';

SELECT * FROM getTopVentas(2018, 2020)