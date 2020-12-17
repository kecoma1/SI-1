ALTER TABLE orders DROP CONSTRAINT orders_customerid_fkey;
ALTER TABLE orders ADD FOREIGN KEY (customerid) REFERENCES customers(customerid) ON UPDATE cascade;

ALTER TABLE orderdetail DROP CONSTRAINT orderdetail_orderid_fkey;
ALTER TABLE orderdetail ADD FOREIGN key (orderid) REFERENCES orders(orderid) ON UPDATE cascade;