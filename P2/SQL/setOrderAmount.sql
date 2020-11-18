CREATE OR REPLACE PROCEDURE setOrderAmount()

LANGUAGE 'plpgsql'

AS $$

BEGIN
	UPDATE 	orders as a
	SET 	netamount = t.sumprice,
		totalamount = t.sumprice+t.sumprice*(tax/100)
	FROM 	(
			--Consulta para obtener el precio total de cada venta
			SELECT sum(price_by_quantity.prc_of_each_detail) AS sumprice, price_by_quantity.order_id_per_detail AS ord_id
			FROM orders AS a, (
						--Consulta para obtener el precio*quantity de cada producto
						SELECT price*quantity as prc_of_each_detail, orderid as order_id_per_detail 
						FROM orderdetail
					) as price_by_quantity
			WHERE price_by_quantity.order_id_per_detail = a.orderid 
			GROUP BY a.orderid, price_by_quantity.order_id_per_detail
		) AS t
	WHERE 	t.ord_id = a.orderid AND (totalamount IS NULL AND netamount IS NULL);

END;
$$;

CALL setOrderAmount();

select * from orders 