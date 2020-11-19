CREATE OR REPLACE FUNCTION getTopMonths (num_products_umbral INTEGER, importe_umbral INTEGER)
RETURNS TABLE (
IMPORTE		NUMERIC,
MES		DOUBLE PRECISION,
ANO		DOUBLE PRECISION,
PRODUCTOS	NUMERIC
)
AS $$

BEGIN

RETURN QUERY	
	-- Sumamos los todos los precios y la cantidad de productos agrupandola en meses
	SELECT SUM(t.importe_consulta), t.mes_consulta as mes, t.ano_consulta as ano, SUM(t.productos_consulta)
	FROM 	(
		-- Agrupamos los orderdetails haciendo un join con ordeid por año y mes. Obtenemos los precios y la cantidad de productos en cada order
		SELECT sum(a.totalamount) AS importe_consulta, EXTRACT(MONTH FROM a.orderdate) AS mes_consulta, EXTRACT(YEAR FROM a.orderdate) AS ano_consulta, COUNT(b.orderid)*quantity as productos_consulta
		FROM orders as a, orderdetail as b
		WHERE b.orderid = a.orderid
		GROUP BY EXTRACT(YEAR FROM orderdate), orderdate, quantity
		) AS t
	GROUP BY mes, ano
	HAVING SUM(t.importe_consulta) > importe_umbral OR SUM(t.productos_consulta) > num_products_umbral;
	
END; $$

LANGUAGE 'plpgsql';

SELECT * FROM getTopMonths(19000, 320000)
