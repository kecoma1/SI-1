-- Modificamos la tabla customers
ALTER TABLE customers ADD COLUMN promo DECIMAL(4,2);

-- Creamos el trigger
DROP TRIGGER IF EXISTS updPromo ON customers;

CREATE OR REPLACE FUNCTION updPromo()
RETURNS TRIGGER AS
$$
	BEGIN
        IF(TG_OP = 'UPDATE') THEN
				-- Actualizamos los orderdetails
				UPDATE orderdetail AS b
				SET price = price - price * (NEW.promo/100)
				FROM orders AS a
				WHERE a.customerid = NEW.customerid AND a.orderid = b.orderid AND a.status IS NULL;

				-- Actualizamos las orders
				UPDATE orders AS a
					SET netamount = t.t_price, 
						totalamount = t.t_price + (a.tax/100) * t.t_price
					FROM 	(
						-- Precio total tras aplicar el descuento después de 
						SELECT c.orderid AS t_id, SUM(c.price) AS t_price
						FROM orderdetail AS c, orders AS d
						WHERE c.orderid = d.orderid AND d.customerid = NEW.customerid AND d.status IS NULL
						GROUP BY c.orderid
						) AS t
					WHERE a.customerid = NEW.customerid AND a.status is NULL AND t.t_id = a.orderid;
				
				-- Sleep tras haber modificado los datos
				PERFORM pg_sleep(20);
					
			RETURN NEW;
	END IF;
	END
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER updPromo
AFTER UPDATE OF promo ON customers
FOR EACH ROW
EXECUTE PROCEDURE updPromo();


-- Creamos carritos
UPDATE orders set status = NULL where customerid=1;
UPDATE orders set status = NULL where customerid=2;
UPDATE orders set status = NULL where customerid=3;
