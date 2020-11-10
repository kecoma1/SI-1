DROP TRIGGER IF EXISTS updOrders ON orderdetail;

CREATE OR REPLACE FUNCTION setOrderAmountId() 
RETURNS TRIGGER 
AS $$
    BEGIN
	IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
		UPDATE orders
        SET netamount = t.precio
        FROM    (
                    SELECT SUM(a.price) AS precio, b.orderid AS id
                    FROM orderdetail AS a, orders AS b
                    WHERE a.orderid = b.orderid
                ) AS t
        WHERE NEW.orderid = t.id
        RETURN NULL
    ELSE
        RETURN NULL

CREATE TRIGGER updOrders
AFTER UPDATE OR INSERT OR DELETE ON orderdetail
FOR EACH ROW
EXECUTE PROCEDURE setOrderAmountId();