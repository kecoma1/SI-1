DROP TRIGGER IF EXISTS updInventory ON orders;

CREATE VIEW cantidad AS
SELECT a.quantity
FROM orderdetail AS a, products AS b 
WHERE a.prod_id = b.prod_id;

CREATE VIEW tienda AS
SELECT a.stock
FROM inventory AS a, products AS b
WHERE a.prod_id = b.prod_id;

CREATE OR REPLACE FUNCTION updInventory()

RETURNS TRIGGER AS 
$$
    BEGIN
        IF (TG_OP = 'UPDATE') THEN
            IF (NEW.state = 'paid') THEN
                -- Comprobar si hay stock
                
                
            END IF;
        END IF;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER updInventory
AFTER UPDATE ON orders
FOR EACH ROW
EXECUTE PROCEDURE updOrders();