------- SOLUCIONANDO ERRORES DE CLAVES QUE FALTAN Y DUPLICACDOS --------

-- Para evitar problemas con setPrice.sql
update imdb_movies set year = '1999' where year = '1998-1999';

-- Añadir claves externas en orders
alter table orders add foreign key (customerid) references customers(customerid) on delete set null on update cascade;

-- Eliminar todos los duplicados en orderdetail para después poner orderid y prod_id como claves primarias
delete from orderdetail where orderid in (
    select orderid
    from (
        select orderid, ROW_NUMBER() OVER (partition by orderid, prod_id order by orderid) as row_num
        from orderdetail
    ) as t
    where t.row_num > 1
);

-- Establecer la clave primaria y secundaria de orderdetail
alter table orderdetail add primary key (orderid, prod_id);
alter table orderdetail add foreign key (orderid) references orders(orderid) on delete cascade on update cascade;
alter table orderdetail add foreign key (prod_id) references products(prod_id) on delete cascade on update cascade;

-- Eliminar la restricción de clave primaria de inventory
alter table inventory drop constraint inventory_pkey;

-- Establecer prod_id en inventory como clave externa
alter table inventory add foreign key (prod_id) references products(prod_id) on delete cascade on update cascade;

-- Añadir la restricción not null a año en imdb_movies
alter table imdb_movies alter column year set not null;

-- Estableciendo la clave primaria de imdb_movielanguages correctamente
alter table imdb_movielanguages drop constraint imdb_movielanguages_pkey;
alter table imdb_movielanguages add primary key (movieid, language);

-- Establecer la clave primaria y secundaria de imdb_actormovies
alter table imdb_actormovies add primary key (actorid, movieid);
alter table imdb_actormovies add foreign key (actorid) references imdb_actors(actorid) on delete cascade on update cascade;
alter table imdb_actormovies add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;

------ ESTABLECIENDO A CASCADE TODAS LAS CLAVES EXTERNAS QUE NO LO ESTÁN Y QUE DEBERÍAN -------

-- Establecer la clave externa de imdb_movies con cascade
alter table products drop constraint products_movieid_fkey;
alter table products add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;

-- Establecer la clave externa de imdb_movielanguages con cascade
alter table imdb_movielanguages drop constraint imdb_movielanguages_movieid_fkey;
alter table imdb_movielanguages add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;

-- Establecer la clave externa de imdb_moviecountries con cascade
alter table imdb_moviecountries drop constraint imdb_moviecountries_movieid_fkey;
alter table imdb_moviecountries add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;

-- Establecer la clave externa de imdb_moviegenres con cascade
alter table imdb_moviegenres drop constraint imdb_moviegenres_movieid_fkey;
alter table imdb_moviegenres add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;

-- Establecer las claves externas de imdb_directormovies con cascade
alter table imdb_directormovies drop constraint imdb_directormovies_movieid_fkey;
alter table imdb_directormovies add foreign key (movieid) references imdb_movies(movieid) on delete cascade on update cascade;
alter table imdb_directormovies add foreign key (directorid) references imdb_directors(directorid) on delete cascade on update cascade;

----------- SOLUCIONANDO INTEGRIDAD DEL DISEÑO --------------

-- Creando la tabla imdb_language e insertando los valores
create table imdb_language(
    language varchar primary key
);

insert into imdb_language(
    select distinct language
    from imdb_movielanguages
);

-- Creando la tabla imdb_genre e insertando los valores
create table imdb_genre(
    genre varchar primary key
);

insert into imdb_genre(
    select distinct genre
    from imdb_moviegenres
);

-- Creando la tabla imdb_country e insertando los valores
create table imdb_country(
    country varchar primary key
);

insert into imdb_country(
    select distinct country
    from imdb_moviecountries
);

-- Estableciendo las claves externas de las tablas creadas

alter table imdb_movielanguages add foreign key (language) references imdb_language(language) on delete cascade on update cascade;

alter table imdb_moviecountries add foreign key (country) references imdb_country(country) on delete cascade on update cascade;

alter table imdb_moviegenres add foreign key (genre) references imdb_genre(genre) on delete cascade on update cascade;

-- Creando la tabla alerta
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

