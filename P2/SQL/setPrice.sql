UPDATE orderdetail
SET price = a.price/POWER(1.02, 2020-CAST(b.year AS INT) )
FROM products AS a, imdb_movies AS b
WHERE orderdetail.prod_id = a.prod_id AND b.movieid = a.movieid

-- Si en 2020 una pelicula vale 30€ ¿Cuanto valía en los 2000 si el precio ha ido aumentando un 2%?
-- 2020 = 30,00 | 2000 = ¿x? |-> 30 = x * 1,02²⁰²⁰⁻²⁰⁰⁰ -> x = 30/1,02²⁰²⁰⁻²⁰⁰⁰