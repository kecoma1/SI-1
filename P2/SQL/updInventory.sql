DROP TRIGGER IF EXISTS updOrders ON updInventory;

CREATE TRIGGER updInventory
AFTER UPDATE ON inventory
FOR EACH ROW
BEGIN
    INSERT INTO alerta (producto_id, 'Stock finalizado', now())
        (
            SELECT prod_id as producto_id FROM products AS a, alerta AS b
            WHERE a.prod_id = b.prod_id
        )
END