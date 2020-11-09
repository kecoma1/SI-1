UPDATE orderdetail
SET price = POWER(1.02, 2020-CAST(b.year AS INT) )*a.price
FROM products AS a, imdb_movies AS b
WHERE orderdetail.prod_id = a.prod_id AND b.movieid = a.movieid
