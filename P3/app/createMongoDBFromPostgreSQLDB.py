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

def db_top_usa_films():
    """
        Función que nos devuelve las peliculas mas actuales de 
        USA (800)

        Return:
            Devuelve True en caso de exito,
            devuelve False en caso de error
    """
    try:
        """
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["si1"]

        mycol = mydb["topUSA"]
        mycol.delete_many({})
        """
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
        mainlist = []

        list_db_result = list(db_result)
        for value in list_db_result:
            maindic = {}
            maindic['title'] = value[1]
            db_genres_list = db_genres(value[0])
            maindic['genres'] = db_genres_list
            maindic['year'] = value[2]
            maindic['directors'] = db_directors(value[0])
            maindic['actors'] = db_actors(value[0]) # Se puede limitar
            maindic['most_related_movies'] = db_most_related(db_genres_list, db_result)
            maindic['related_movies'] = db_related(db_genres_list, db_result)
            mainlist.append(maindic)

        return mainlist
       
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
                                    where imdb_moviegenres.movieid = '"+str(id)+"'") 
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
                                    and imdb_directormovies.movieid = '"+str(id)+"'") 
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
                                    imdb_actormovies.movieid = '"+str(id)+"'\
                                    limit 5") 
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


def db_most_related(lista, tuplas):
    """
    Función que nos devuelve una lista con las películas que tengan mismo generos
    Return:
        Devuelve una lista en caso de exito,
        devuelve False en caso de error
    """
    if lista == None or tuplas == None:
        return False

    most_related_list = []
    most_related_dic = {}
    counter = 0
    for value in tuplas:
        if lista == db_genres(value[0]):
            most_related_dic['title'] = value[1]
            most_related_dic['year'] = value[2]
            most_related_list.append(most_related_dic)
            counter += 1

        if counter >= 10:
            break
    
    return most_related_list


def db_related(lista, tuplas):
    """
    Función que nos devuelve una lista con las películas que tengan relación
    Return:
        Devuelve una lista en caso de exito,
        devuelve False en caso de error
    """

    if lista == None or tuplas == None:
        return False

    length = len(lista)
    related_list = []

    if length == 1:
        return related_list

    related_dic = {}
    counter = 0
    for value in tuplas:

        matches = 0
        genres_list = db_genres(value[0])
        for genre in genres_list:
            if genre in lista:
                matches += 1

        if matches == (length/2):
            related_dic['title'] = value[1]
            related_dic['year'] = value[2]
            related_list.append(related_dic)
            counter += 1
            
        if counter >= 10:
            break
    
    return related_list


def main():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["si1"]

    mycol = mydb["topUSA"]
    mycol.drop()

    top_usa = db_top_usa_films()

    mycol.insert_many(top_usa)

if __name__ == '__main__':
    main()