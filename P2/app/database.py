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
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Seleccionar las peliculas mas vendidas en los ultimos 3 anos
        db_result = db_conn.execute("SELECT * FROM getTopVentas(2004, 2006)")
        db_conn.close()

        # Convertimos a una lista las peliculas
        result_list = list(db_result)
        pelis_list = []

        db_conn = db_engine.connect()
        
        for film in result_list:
            # Obtener toda la info de las peliculas
            db_movie_info = select([db_table_movies]).where(text("movietitle="+"'"+str(film[1])+"'" ) )
            db_result = db_conn.execute(db_movie_info)
            pelis_list.append(list(db_result))
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

