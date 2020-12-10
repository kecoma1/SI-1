# -*- coding: utf-8 -*-
import os
import sys, traceback
import pymongo
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select
import datetime
import random

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)

def db_top_films():
    """
        Función que nos devuelve las peliculas mas actuales de 
        USA (800)

        Return:
            Devuelve True en caso de exito,
            devuelve False en caso de error
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Obtiene los ids de las 800 películas estadounidenses mas nuevas
        db_result = db_conn.execute("select imdb_movies.movieid, movietitle, year\
                                    from imdb_movies, imdb_moviecountries\
                                    where imdb_movies.movieid = imdb_moviecountries.movieid\
                                    and imdb_moviecountries.country = 'USA'\
                                    order by imdb_movies.year\
                                    desc\
                                    limit 800")
        db_conn.close()

        # Obtenemos los valores buscados para meter en la base mongodb
        movieid_list = []
        title_list = []
        year_list = []
        for value in db_result:
            # print(value[0])
            movieid_list.append(value[0])
            title_list.append(value[1])
            year_list.append(value[2])

        # print(year_list)

        genres_list = db_genres(movieid_list)
        

        # Convertimos a una lista las peliculas
        pelis_list = []
       
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_genres(id):
    """
    Función que nos devuelve una lista con los generos de la película

    Return:
        Devuelve una lista en caso de exito,
        devuelve False en caso de error
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtiene los genres de la movieid que pasamos
        db_result = db_conn.execute("select imdb_moviegenres.genre\
                                    from imdb_moviegenres\
                                    where imdb_moviegenres.movieid = '"+id+"'") 
        db_conn.close()
        
        # Pasamos los valores de tupla a lista
        genre_list = []
        for value in db_result:
            genre_list.append(value[0])

        return genre_list
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_directors(id):
    """
    Función que nos devuelve una lista con los directores de la película

    Return:
        Devuelve una lista en caso de exito,
        devuelve False en caso de error
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtiene los genres de la movieid que pasamos
        db_result = db_conn.execute("select directorname\
                                    from imdb_directormovies, imdb_directors\
                                    where imdb_directormovies.directorid = imdb_directors.directorid\
                                    and imdb_directormovies.movieid = '"+id+"'") 
        db_conn.close()
        
        # Pasamos los valores de tupla a lista
        directors_list = []
        for value in db_result:
            directors_list.append(value[0])

        return directors_list
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False

def db_actors(id):
    """
    Función que nos devuelve una lista con los directores de la película

    Return:
        Devuelve una lista en caso de exito,
        devuelve False en caso de error
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtiene los genres de la movieid que pasamos
        db_result = db_conn.execute("select actorname\
                                    from imdb_actormovies, imdb_actors\
                                    where imdb_actormovies.actorid = imdb_actors.actorid and\
                                    imdb_actormovies.movieid = '"+id+"'") 
        db_conn.close()
        
        # Pasamos los valores de tupla a lista
        actors_list = []
        for value in db_result:
            actors_list.append(value[0])

        return actors_list
        
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["si1"]

mycol = mydb["topUSA"]

db_top_films()