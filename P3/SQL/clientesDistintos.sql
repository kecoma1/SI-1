SELECT COUNT(a.customerid) FROM customers AS a, orders as b
WHERE a.customerid = b.customerid AND EXTRACT(YEAR FROM b.orderdate) = 2015 AND EXTRACT(MONTH FROM b.orderdate) = 4 AND b.totalamount > 100
