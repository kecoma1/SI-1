# -*- coding: utf-8 -*-
import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)
# cargar una tabla
db_table_movies = Table('imdb_movies', db_meta, autoload=True, autoload_with=db_engine)
db_imdb_actormovies = Table('imdb_actormovies', db_meta, autoload=True, autoload_with=db_engine)
db_imdb_actors = Table('imdb_actors', db_meta, autoload=True, autoload_with=db_engine)
db_imdb_directormovies = Table('imdb_directormovies', db_meta, autoload=True, autoload_with=db_engine)
db_imdb_directors = Table('imdb_directors', db_meta, autoload=True, autoload_with=db_engine)

def de_tupla_lista(tupla):
    """
        Función que convierte una tupla a una list
    """
    lista = []

    # Introducimos valores en la lista
    for valor in tupla:
        lista.append(valor)
        
    return lista

def db_listOfMovies1949():
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Seleccionar las peliculas del anno 1949
        db_movies_1949 = select([db_table_movies]).where(text("year = '1949'"))
        db_result = db_conn.execute(db_movies_1949)
        #db_result = db_conn.execute("Select * from getTopVentas()")
        
        db_conn.close()
        
        return  list(db_result)
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def db_top_films():
    """
        Función que nos devuelve las topfilms de los últimos 3 anos
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Seleccionar las peliculas mas vendidas en los ultimos 3 anos
        db_result = db_conn.execute("SELECT * FROM getTopVentas(2004, 2006)")
        db_conn.close()
        resultlist = list(db_result)
        # Convertimos a una lista las peliculas
        pelis_list = []

        db_conn = db_engine.connect()
        i = 0
        for film in resultlist:
            # Obtener toda la info de las peliculas
            db_movie_info = select([db_table_movies]).where(text("movietitle="+"'"+str(film[1])+"'" ) )
            db_result = db_conn.execute(db_movie_info)
            # Traducimos el return de db_conn.execute
            pelis_list.append([])
            for tupla in list(db_result):
                pelis_list[i] = de_tupla_lista(tupla)
            i += 1
        db_conn.close()
        return pelis_list
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def getPelicula(id):
    """
        Función que devuelve la info de una pelicula
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
    
        # Obtener toda la info de las peliculas
        db_movie_info = select([db_table_movies]).where(text("movieid="+"'"+id+"'" ) )
        db_result = db_conn.execute(db_movie_info)
        
        pelicula = de_tupla_lista(list(db_result)[0])

        db_conn.close()
        return pelicula
            
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def getDirectores(id):
    """
        Función que nos devuelve los directores de una 
        pelicula dada
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
    
        # Obtener el nombre del director de la película
        db_result = db_conn.execute("select directorname\
            from imdb_directors, imdb_directormovies\
            where imdb_directors.directorid = imdb_directormovies.directorid\
            and imdb_directormovies.movieid = "+id)
        db_conn.close()
        
        directores_lista = []
        i = 0
        for directores in list(db_result):
            # Traducimos el return de db_conn.execute
            directores_lista.append([])
            directores_lista[i] = directores[0]
            i += 1

        db_conn.close()
        return directores_lista  
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def getActores(id):
    """
        Función que nos devuelve los actores de una 
        pelicula dada
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
    
        # Obtener todos los actores de la película
        db_result = db_conn.execute("select c.actorname, b.character\
        from imdb_actormovies as b, imdb_actors as c\
        where b.movieid = "+id+" and b.actorid = c.actorid")
        db_conn.close()
        
        actores_lista = []
        i = 0
        for actores in list(db_result):
            # Traducimos el return de db_conn.execute
            actores_lista.append([])
            actores_lista[i] = de_tupla_lista(actores)
            i += 1

        db_conn.close()
        return actores_lista
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def getPrecio(id):
    """
        Funcion que nos devuelve el precio de una 
        pelicula dada
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
    
        # Obtener el nombre el precio de la película
        db_result = db_conn.execute(
            "select price, p.description from imdb_movies as m, products as p where m.movieid=p.movieid and m.movieid = "+id
        )

        precios_list = []
        i = 0
        for precios in list(db_result):
            precios_list.append([])
            precios_list[i] = de_tupla_lista(precios)
            i += 1

        db_conn.close()
        return precios_list
            
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return 'Something is broken'

def validar