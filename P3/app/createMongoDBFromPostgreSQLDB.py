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
db_conn = None

def db_top_usa_films():
    """
        Función que nos devuelve las peliculas mas actuales de 
        USA (800)

        Return:
            Devuelve una lista con las películas en caso de exito,
            devuelve False en caso de error
    """
    try:
        i = 1
        
        # Obtiene los ids de las 800 películas estadounidenses mas nuevas
        db_result = db_conn.execute("select imdb_movies.movieid, movietitle, year\
                                    from imdb_movies, imdb_moviecountries\
                                    where imdb_movies.movieid = imdb_moviecountries.movieid\
                                    and imdb_moviecountries.country = 'USA'\
                                    order by imdb_movies.year\
                                    desc\
                                    limit 800")

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
            maindic['most_related_movies'] = db_most_related(value[0], db_genres_list, list_db_result)
            maindic['related_movies'] = db_related(value[0], db_genres_list, list_db_result)
            mainlist.append(maindic)
            print("\tPelicula ", i, " de 800")
            i+=1
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

    Args:
        id (int): Entero con la id de la película

    Return:
        Devuelve una lista con los géneros en caso de exito,
        devuelve False en caso de error
    """
    try:

        # Obtiene los genres de la movieid que pasamos
        db_result = db_conn.execute("select imdb_moviegenres.genre\
                                    from imdb_moviegenres\
                                    where imdb_moviegenres.movieid = '"+str(id)+"'") 
        
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

    Args:
        id (int): Entero con la id de la película

    Return:
        Devuelve una lista en caso de exito,
        devuelve False en caso de error
    """
    try:

        # Obtiene los directores de la movieid que pasamos
        db_result = db_conn.execute("select directorname\
                                    from imdb_directormovies, imdb_directors\
                                    where imdb_directormovies.directorid = imdb_directors.directorid\
                                    and imdb_directormovies.movieid = '"+str(id)+"'") 
        
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

    Args:
        id (int): Entero con la id de la película

    Return:
        Devuelve una lista en caso de exito,
        devuelve False en caso de error
    """
    try:

        # Obtiene los actores de la movieid que pasamos
        db_result = db_conn.execute("select actorname\
                                    from imdb_actormovies, imdb_actors\
                                    where imdb_actormovies.actorid = imdb_actors.actorid and\
                                    imdb_actormovies.movieid = '"+str(id)+"'\
                                    limit 5") 
        
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


def db_most_related(id, lista, tuplas):
    """
    Función que nos devuelve una lista con las películas que tengan el 100%
    de los generos de la película 'x'

    Args:
        id (int): Entero con la id de la película (usado para no anadir la misma pelicula)
        lista (list): Lista con los generos de la película 'x'
        tuplas (lista de tuplas): Lista con las 800 películas del topUsa

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
        # Comprobamos si la lista es igual a los géneros
        if  all(item in db_genres(value[0]) for item in lista) and id != value[0]:
            # Actualizamos el diccionario
            most_related_dic = {}
            most_related_dic['title'] = value[1]
            most_related_dic['year'] = value[2]
            most_related_list.append(most_related_dic)
            counter += 1

        # Si llegamos a 10 peliculas que sean related salimos del loop 
        if counter >= 10:
            break
    
    return most_related_list


def db_related(id, lista, tuplas):
    """
    Función que nos devuelve una lista con las películas que tengan relación, 
    el 50% (aprox.) de las películas

    Args:
        id (int): Entero con la id de la película (usado para no anadir la misma pelicula)
        lista (list): Lista con los generos de la película 'x'
        tuplas (lista de tuplas): Lista con las 800 películas del topUsa

    Return:
        Devuelve una lista en caso de exito,
        devuelve False en caso de error
    """

    if lista == None or tuplas == None:
        return False

    length = len(lista)
    if length == 0:
        return []
    related_list = []
    counter = 0
    for value in tuplas:

        matches = 0
        genres_list = db_genres(value[0])
        # Comprobamos los generos
        for genre in genres_list:
            # Si el genero esta en la lista de la peli, matches++
            if genre in lista:
                matches += 1

        # Evitamos divisiones entre 0
        if matches == 0:
            continue

        # Si los matches son el 50%, actualizamos el diccionario
        if (length/matches >= 1.5 and length/matches <= 2) and id != list(value)[0]:
            related_dic = {}
            related_dic['title'] = value[1]
            related_dic['year'] = value[2]
            related_list.append(related_dic)
            counter += 1
           
        # Si llegamos a 10 peliculas que sean related salimos del loop 
        if counter >= 10:
            break
    
    return related_list


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["si1"]

# En caso de que exista la eliminamos
mycol = mydb["topUSA"]
mycol.drop()

# La volvemos a crear
mycol = mydb["topUSA"]

# conexion a la base de datos
db_conn = None
db_conn = db_engine.connect()

print("Registramos las peliculas de la BD")
top_usa = db_top_usa_films()

db_conn.close()

print("Insertamos las peliculas en mongodb")
mycol.insert_many(top_usa)

prueba = mycol.find({'directors': {'$elemMatch': {'$regex': 'Allen, Woody'}}})
#print(list(prueba))
#print(list(second_table))
# print(second_table)
