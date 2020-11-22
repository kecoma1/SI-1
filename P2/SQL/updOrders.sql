DROP TRIGGER IF EXISTS updOrders ON orderdetail;

CREATE OR REPLACE FUNCTION updOrders()
RETURNS TRIGGER AS
$$
	BEGIN
		IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE' OR TG_OP = 'DELETE') THEN
		UPDATE orders
		-- Actualizamos el valor con el precio correcto
		SET netamount = t.precio, totalamount = t.precio+t.precio*((tax/100))
		FROM    
			(
			-- Calculamos el total de la orden
			SELECT SUM(t0.total) as precio
			FROM	(
					-- Calculamos precio por producto
					SELECT quantity*price AS total 
					FROM orderdetail 
					WHERE orderid = NEW.orderid
				) as t0
			) AS t;
			
			RETURN NEW;
		ELSE
			RETURN NULL;
		END IF;
	END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER updOrders
AFTER UPDATE OR INSERT OR DELETE ON orderdetail
FOR EACH ROW
EXECUTE PROCEDURE updOrders();

select * from orderdetail where orderid = 1 limit 10
select * from orders where orderid = 1
update orderdetail set price = 3 where orderid = 1