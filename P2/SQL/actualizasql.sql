-- Add foreign key in orders
alter table orders add foreign key (customerid) references customers(customerid);

-- Add not null to the previous foreign key
alter table orders alter column customerid set not null;

-- Delete all the duplicates in orderdetail to later on set orderid and prod_id as primary keys
delete from orderdetail where orderid in (
    select orderid
    from (
        select orderid, ROW_NUMBER() OVER (partition by orderid, prod_id order by orderid) as row_num
        from orderdetail
    ) as t
    where t.row_num > 1
);

-- Set orderid and prod_id as primary key
alter table orderdetail add PRIMARY key (orderid, prod_id);

-- Eliminate the primary key constraint in inventory
alter table inventory drop constraint inventory_pkey;

-- Set prod_id in inventory as foreign key
alter table inventory add foreign key (prod_id) references products(prod_id);

-- Add not null constraint to year in imdb_movies
alter table imdb_movies alter column year set not null;

-- Resetting the primary key value correctly
alter table imdb_movielanguages drop constraint imdb_movielanguages_pkey;
alter table imdb_movielanguages add primary key (movieid, language);

-- Set the primary key and foreign keys of imdb_actormovies
alter table imdb_actormovies add primary key (actorid, movieid);
alter table imdb_actormovies add foreign key (actorid) references imdb_actor(actorid);
alter table imdb_actormovies add foreign key (movieid) references imdb_movies(movieid);

