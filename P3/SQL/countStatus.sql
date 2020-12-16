explain select count(*) from orders where status is null;
--Aggregate  (cost=3507.17..3507.18 rows=1 width=8)
--  ->  Seq Scan on orders  (cost=0.00..3504.90 rows=909 width=0)
--        Filter: (status IS NULL)

CREATE INDEX index_status ON orders(status)

explain select count(*) from orders where status is null;
--Aggregate  (cost=1496.52..1496.53 rows=1 width=8)
--  ->  Bitmap Heap Scan on orders  (cost=19.46..1494.25 rows=909 width=0)
--        Recheck Cond: (status IS NULL)
--        ->  Bitmap Index Scan on index_status  (cost=0.00..19.24 rows=909 width=0)
--              Index Cond: (status IS NULL)

ANALYZE orders

explain select count(*) from orders where status is null;
--Aggregate  (cost=7.33..7.34 rows=1 width=8)
--  ->  Index Only Scan using index_status on orders  (cost=0.42..7.32 rows=1 width=0)
--        Index Cond: (status IS NULL)
