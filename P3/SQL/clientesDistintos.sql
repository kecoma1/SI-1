-- Consulta para obtener el número de clientes distintos que han hecho una compra en el mes 4 de 2015 y que el total sea mayor que 100
SELECT COUNT(a.customerid) FROM customers AS a, orders as b
WHERE a.customerid = b.customerid AND EXTRACT(YEAR FROM b.orderdate) = 2015 AND EXTRACT(MONTH FROM b.orderdate) = 4 AND b.totalamount > 100

EXPLAIN SELECT COUNT(a.customerid) FROM customers AS a, orders as b
WHERE a.customerid = b.customerid AND EXTRACT(YEAR FROM b.orderdate) = 2015 AND EXTRACT(MONTH FROM b.orderdate) = 4 AND b.totalamount > 100
--Finalize Aggregate  (cost=5636.14..5636.15 rows=1 width=8)
--  ->  Gather  (cost=5636.03..5636.14 rows=1 width=8)
--        Workers Planned: 1
--        ->  Partial Aggregate  (cost=4636.03..4636.04 rows=1 width=8)
--              ->  Nested Loop  (cost=0.29..4636.02 rows=1 width=4)
--                    ->  Parallel Seq Scan on orders b  (cost=0.00..4627.72 rows=1 width=4)
--                          Filter: ((totalamount > '100'::numeric) AND (date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double preci (...)
--                    ->  Index Only Scan using customers_pkey on customers a  (cost=0.29..8.30 rows=1 width=4)
--                          Index Cond: (customerid = b.customerid)

-- La primary key es un index implicito

-- Creamos un index en orderdate
CREATE INDEX index_orderdate ON orders(orderdate)

EXPLAIN SELECT COUNT(a.customerid) FROM customers AS a, orders as b
WHERE a.customerid = b.customerid AND EXTRACT(YEAR FROM b.orderdate) = 2015 AND EXTRACT(MONTH FROM b.orderdate) = 4 AND b.totalamount > 100
--Finalize Aggregate  (cost=5636.14..5636.15 rows=1 width=8)
--  ->  Gather  (cost=5636.03..5636.14 rows=1 width=8)
--        Workers Planned: 1
--        ->  Partial Aggregate  (cost=4636.03..4636.04 rows=1 width=8)
--              ->  Nested Loop  (cost=0.29..4636.02 rows=1 width=4)
--                    ->  Parallel Seq Scan on orders b  (cost=0.00..4627.72 rows=1 width=4)
--                          Filter: ((totalamount > '100'::numeric) AND (date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double preci (...)
--                    ->  Index Only Scan using customers_pkey on customers a  (cost=0.29..8.30 rows=1 width=4)
--                          Index Cond: (customerid = b.customerid)
-- Al parecer el index en orderdate es irrelevante, la estructura de la ejecución es la misa
DROP INDEX index_orderdate

-- Creamos un indice en el total amount
CREATE INDEX index_totalamount ON orders(totalamount)

EXPLAIN SELECT COUNT(a.customerid) FROM customers AS a, orders as b
WHERE a.customerid = b.customerid AND EXTRACT(YEAR FROM b.orderdate) = 2015 AND EXTRACT(MONTH FROM b.orderdate) = 4 AND b.totalamount > 100
--Aggregate  (cost=4496.93..4496.94 rows=1 width=8)
--  ->  Nested Loop  (cost=1127.18..4496.92 rows=2 width=4)
--        ->  Bitmap Heap Scan on orders b  (cost=1126.90..4480.32 rows=2 width=4)
--              Recheck Cond: (totalamount > '100'::numeric)
--              Filter: ((date_part('year'::text, (orderdate)::timestamp without time zone) = '2015'::double precision) AND (date_part('month'::text, (orderdate)::timestamp without time zone) = '4'::double precision))
--              ->  Bitmap Index Scan on index_totalamount  (cost=0.00..1126.90 rows=60597 width=0)
--                    Index Cond: (totalamount > '100'::numeric)
--        ->  Index Only Scan using customers_pkey on customers a  (cost=0.29..8.30 rows=1 width=4)
--              Index Cond: (customerid = b.customerid)
-- Podemos ver que el coste ha disminuido, ha desaparecido el parcial agregate, del filtro se ha eliminado el mayor que 100 pero se ha creado un bitmap para comprobar dicha condición
DROP INDEX index_totalamount

--¿Podríamos crear más indexs? No, seria innecesario crear un indice donde no hace falta, ya hemos creado indices en las columnas donde pueden ser utiles (las primary keys son indices implicitos).
