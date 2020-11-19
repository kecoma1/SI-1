------- FIXING MISTAKES RELATED TO MISSING KEYS AND DUPLICATES --------

-- To avoid problems in setPrice.sql
update imdb_movies set year = '1999' where year = '1998-1999';

-- Add foreign key in orders
alter table orders add foreign key (customerid) references customers(customerid) on delete set null on update cascade;

-- Delete all the duplicates in orderdetail to later on set orderid and prod_id as primary keys
delete from orderdetail where orderid in (
    select orderid
    from (
        select orderid, ROW_NUMBER() OVER (partition by orderid, prod_id order by orderid) as row_num
        from orderdetail
    ) as t
    where t.row_num > 1
);

-- Set primary key and foreign keys of orderdetail
alter table orderdetail add primary key (orderid, prod_id);
alter table orderdetail add foreign key (orderid) references orders(orderid) on delete cascade on update cascade;
alter table orderdetail add foreign key (prod_id) references products(prod_id) on delete cascade on update cascade;

-- Eliminate the primary key constraint in inventory
alter table inventory drop constraint inventory_pkey;

-- Set prod_id in inventory as foreign key
alter table inventory add foreign key (prod_id) references products(prod_id) on delete cascade on update cascade;

-- Add not null constraint to year in imdb_movies
alter table imdb_movies alter column year set not null;

-- Resetting the primary key value correctly
alter table imdb_movielanguages drop constraint imdb_movielanguages_pkey;
alter table imdb_movielanguages add primary key (movieid, language);

-- Set the primary key and foreign keys of imdb_actormovies
alter table imdb_actormovies add primary key (actorid, movieid);
alter table imdb_actormovies add foreign key (actorid) references imdb_actors(actorid) on delete cascade on update cascade;
alter table imdb_actormovies add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;

------ SETTING TO CASCADE ALL THE FOREIGN KEYS THAT WEREN'T AND MUST BE -------

-- Set the foreign key of imdb_movies on cascade
alter table products drop constraint products_movieid_fkey;
alter table products add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;

-- Set the foreign key of imdb_movieslanguages on cascade
alter table imdb_movielanguages drop constraint imdb_movielanguages_movieid_fkey;
alter table imdb_movielanguages add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;

-- Set the foreign key of imdb_moviescountries on cascade
alter table imdb_moviecountries drop constraint imdb_moviecountries_movieid_fkey;
alter table imdb_moviecountries add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;

-- Set the foreign key of imdb_moviesgenres on cascade
alter table imdb_moviegenres drop constraint imdb_moviegenres_movieid_fkey;
alter table imdb_moviegenres add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;

-- Set the foreign key of imdb_directormovies on cascade
alter table imdb_directormovies drop constraint imdb_directormovies_movieid_fkey;
alter table imdb_directormovies add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;
alter table imdb_directormovies add foreign key (directorid) references imdb_directors(directorid) on delete cascade on update cascade;

----------- SOLUCIONANDO INTEGRIDAD DEL DISEÑO --------------

create table imdb_language(
    language varchar primary key
);

insert into imdb_language(
    select distinct language
    from imdb_movielanguages
);

create table imdb_genre(
    genre varchar primary key
);

insert into imdb_genre(
    select distinct genre
    from imdb_moviegenres
);

create table imdb_country(
    country varchar primary key
);

insert into imdb_country(
    select distinct country
    from imdb_moviecountries
);

-- Setting all the needed foreign keys

alter table imdb_movielanguages add foreign key (language) references imdb_language(language) on delete cascade on update cascade;

alter table imdb_moviecountries add foreign key (country) references imdb_country(country) on delete cascade on update cascade;

alter table imdb_moviegenres add foreign key (genre) references imdb_genre(genre) on delete cascade on update cascade;

-- Creating the table alert
create table alerta(
    prod_id int references products(prod_id) on delete cascade on update cascade,
    description text not null,
    fecha date not null
);

--
--
-- customerid en orders no tiene la foreign key establecida en cascade para cuando se 
-- elimine ni cuando se actualice porque no tenemos opción de borrar usuario y aun así
-- en tal caso querríamos mantener las orders que haya hecho este usuario.
--
--

