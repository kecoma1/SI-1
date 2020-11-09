CREATE OR REPLACE PROCEDURE setOrderAmount()

LANGUAGE 'plpgsql'

AS $$

BEGIN
	UPDATE 	orders as a
	SET 	netamount = t.sumprice,
		totalamount = t.sumprice+t.sumprice*(tax/100)
	FROM 	(
			SELECT sum(b.price) AS sumprice, a.orderid AS ord_id
			FROM orders AS a, orderdetail AS b
			WHERE b.orderid = a.orderid 
			GROUP BY a.orderid
		) AS t
	WHERE 	t.ord_id = a.orderid AND (totalamount IS NULL OR netamount IS NULL);

END;
$$;

CALL setOrderAmount();

select * from orders
