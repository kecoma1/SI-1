ALTER TABLE customers ADD COLUMN promo DECIMAL(4,2);

DROP TRIGGER IF EXISTS updPromo ON customers;

CREATE OR REPLACE FUNCTION updPromo()
RETURNS TRIGGER AS
$$
	BEGIN
        IF(TG_OP = 'UPDATE') THEN
        			UPDATE orderdetail AS b
						SET price = price - price * (NEW.promo/100)
						FROM orders AS a
						WHERE a.customerid = 1 AND a.orderid = b.orderid AND a.status IS NULL;
			RETURN NEW;
	END IF;
	END
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER updPromo
AFTER UPDATE ON customers
FOR EACH ROW
EXECUTE PROCEDURE updPromo();