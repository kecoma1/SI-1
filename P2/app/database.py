# -*- coding: utf-8 -*-
import os
import sys, traceback
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, text
from sqlalchemy.sql import select
import datetime

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False)
db_meta = MetaData(bind=db_engine)
# cargar una tabla
db_table_movies = Table('imdb_movies', db_meta, autoload=True, autoload_with=db_engine)
db_imdb_actormovies = Table('imdb_actormovies', db_meta, autoload=True, autoload_with=db_engine)
db_imdb_actors = Table('imdb_actors', db_meta, autoload=True, autoload_with=db_engine)
db_imdb_directormovies = Table('imdb_directormovies', db_meta, autoload=True, autoload_with=db_engine)
db_imdb_directors = Table('imdb_directors', db_meta, autoload=True, autoload_with=db_engine)
db_customers = Table('customers', db_meta, autoload=True, autoload_with=db_engine)

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

        Return:
            Devuelve una lista en caso de exito,
            devuelve False en caso de error
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Seleccionar las peliculas mas vendidas en los ultimos 3 anos
        db_result = db_conn.execute("SELECT * FROM getTopVentas(2018, 2020)")
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

        return False


def getPelicula(id):
    """
        Función que devuelve la info de una pelicula

        Return:
            Devuelve una pelicula en caso de exito
            Devuelve False en caso de error
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

        return False


def getDirectores(id):
    """
        Función que nos devuelve los directores de una 
        pelicula dada

        Return:
            Devuelve un director en caso de exito
            Devuelve False en caso de error
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
    
        # Obtener el nombre del director de la película
        db_result = db_conn.execute("SELECT directorname\
            FROM imdb_directors, imdb_directormovies\
            WHERE imdb_directors.directorid = imdb_directormovies.directorid\
            AND imdb_directormovies.movieid = "+id)
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

        return False


def getActores(id):
    """
        Función que nos devuelve los actores de una 
        pelicula dada

        Return:
            Devuelve un actor en caso de exito
            Devuelve False en caso de error
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
    
        # Obtener todos los actores de la película
        db_result = db_conn.execute("SELECT c.actorname, b.character\
        FROM imdb_actormovies AS b, imdb_actors AS c\
        WHERE b.movieid = "+id+" AND b.actorid = c.actorid")
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

        return False


def getPrecio(id):
    """
        Funcion que nos devuelve el precio de una 
        pelicula dada

        Return:
            Devuelve una lista con los precios dependiendo de la edición en caso de exito
            Devuelve False en caso de error
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
    
        # Obtener el nombre el precio de la película
        db_result = db_conn.execute(
            "SELECT price, p.description, p.prod_id FROM imdb_movies AS m, products AS p WHERE m.movieid=p.movieid AND m.movieid = "+id
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

        return False


def validar(username, password):
    """
        Funcion para validar la información del login

        Return:
            Devuelve True en caso de que el username y la password sean correctos,
            en caso de error devuelve False
    """
    # Prevenir sqlinjection
    if "'" in username or "'" in password:
        return
    
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()
        
        # Seleccionar las peliculas del anno 1949
        db_user = select([db_customers]).where(text("username='"+username+"' and password='"+password+"'"))
        db_result = db_conn.execute(db_user)
        
        db_conn.close()

        resultado = list(db_result)[0]
        # Comprobamos que el resultado de la query es correcto
        if resultado[15] == username and resultado[16] == password:
            return True
        else:
            return False
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        return False


def registrar(firstname, lastname, address1, address2, 
                           city, state, zipcode, country, region, email, 
                           phone, creditcardType, creditcard, creditcardexpiration, 
                           username, password, age, income, gender):
    """Función para registrar a un usuario si el username no existe

    Args:
        Información necesaria para registrar al usuario

    Returns:
        Bool: True si se registra, False si no
    """
    # Comprobamos los campos requeridos
    if firstname == "" or lastname == "" or city == "" or zipcode == "" or state == ""\
        or  zipcode == "" or country == "" or creditcard == "" or creditcardexpiration == ""\
        or username == "" or password == "":
            return

    try:
        # Comprobar que el username no existe
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        db_result = db_conn.execute("SELECT * FROM customers WHERE username='"+username+"'")

        # Si hay alguien con el mismo username retornar
        if len(list(db_result)) > 0:
            return False

        # Obtenemos el último customerid para asignar el siguiente
        db_result = db_conn.execute("SELECT customerid FROM customers ORDER BY customerid DESC LIMIT 1")
        customerid = list(db_result)[0][0]
        customerid+=1

        # Insertamos en la tabla el usuario
        db_result = db_conn.execute("INSERT INTO customers (customerid, firstname, lastname, address1, address2,\
                                    city, state, zip, country, region, email,\
                                    phone, creditcardType, creditcard, creditcardexpiration,\
                                    username, password, age, income, gender)\
                                    VALUES ("+str(customerid)+", '"+firstname+"', '"+lastname+"', "+address1+", "+address2+",\
                                    '"+city+"', "+state+", '"+zipcode+"', '"+country+"', '"+region+"', "+email+",\
                                    "+phone+", '"+creditcardType+"', '"+creditcard+"', '"+creditcardexpiration+"', '"+username+"', '"+password+"',\
                                    "+age+", "+income+", "+gender+")")
        db_conn.close()
        return True
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)
        return False


def buscarPeliculas(busqueda):
    """Buscamos las peliculas en las bases de datos dada una string
    Como máximo se cojen 100 películas (sin imágenes)

    Args:
        busqueda (String): String con los nombres a buscar

    Return:
        Devuelve una lista con las peliculas que en su nombre continen la string introducida
        Devuelve la False si hay un error
    """
    # Prevenimos sqlinjection y comprobamos que haya algo que buscar
    if len(busqueda) <= 0 or ("'" in busqueda) or ('"' in busqueda):
        return False

    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Ejecutamos query buscando las peliculas donde este esa string
        db_movie_info = select([db_table_movies]).where(text("movietitle LIKE '%"+busqueda+"%' LIMIT 100" ) )
        db_result = db_conn.execute(db_movie_info)

        pelis_list = []
        i = 0
        for tupla in list(db_result):
            pelis_list.append([])
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
        return False


def categoria(categoria):
    """Función que genera una lista de todas las peliculas 
        con la categoría introducida

    Args:
        categoria (string): String de la categoría

    Return:
        Lista de peliculas con la categoría
    """
    # Comprobamos que el argumento contenga caracteres y prevenimos sqlinjection
    if len(categoria) <= 0 or ("'" in categoria) or ('"' in categoria):
        return False
    
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Ejecutamos query buscando las peliculas que pertenezcan a esa categoria/género
        db_result = db_conn.execute("SELECT a.movieid, a.movietitle FROM imdb_movies as a, imdb_moviegenres as b WHERE a.movieid=b.movieid AND b.genre='"+categoria+"'")

        pelis_list = []
        i = 0
        for tupla in list(db_result):
            pelis_list.append([])
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
        return False

def anadirFilm(id, username):
    """ Función que añade las películas que se quieran comprar en el carrito,
        en el caso de que el usuario haya iniciado sesión

        Args: 
            id (string): Id de la película que esta siendo añadida (producto).
            username (string): Username del customer al que hay que modificar el carrito

        Return:
            Devuelve la movieid o false en caso de error
    """
    orderid = None
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Cogemos el customerid
        db_result = db_conn.execute("SELECT customerid FROM customers WHERE username = '"+username+"'")
        customerid = list(db_result)[0][0]

        # Comprobamos si hay un order a null
        db_result = db_conn.execute("SELECT orderid\
                                    FROM orders AS a, customers AS b\
                                    WHERE b.customerid = a.customerid AND b.username = '"+username+"' AND a.status IS NULL")
        orderid_list = list(db_result)
        
        # No hay carrito
        if len(orderid_list) == 0:
            # Cogemos la ultima orderid
            db_result = db_conn.execute("SELECT orderid FROM orders ORDER BY orderid DESC LIMIT 1")
            orderid = list(db_result)[0][0]
            orderid += 1

            # Creamos una order con status a null
            db_conn.execute("INSERT INTO orders (orderid, customerid, netamount, totalamount, tax, status, orderdate)\
                            VALUES ("+str(orderid)+", "+str(customerid)+", 0, 0, 21, NULL, CURRENT_DATE)")
        else:
            # Obtenemos el orderid del carrito
            orderid = orderid_list[0][0]

        # Obtenemos el precio del producto
        db_result = db_conn.execute("SELECT price FROM products WHERE prod_id = "+id+"")
        price = list(db_result)[0][0]

        # Comprobamos si hay un orderdetail con el mismo producto
        db_result = db_conn.execute("SELECT orderid, prod_id FROM orderdetail WHERE orderid = "+str(orderid)+" AND prod_id = "+id+"")
        if len(list(db_result)) == 0:
            # Anadimos el producto a la orden (crear orderdetail)
            db_conn.execute("INSERT INTO orderdetail (orderid, prod_id, quantity, price)\
                            VALUES ("+str(orderid)+", "+id+", 1, "+str(price)+")")
        else:
            # Si hay solo actualizamos el valor de quantity
            db_conn.execute("UPDATE orderdetail\
                            SET quantity = quantity+1\
                            WHERE orderid = "+str(orderid)+" AND prod_id = "+id+"")
            
        # Cogemos la movieid del producto
        db_result = db_conn.execute("SELECT a.movieid FROM imdb_movies AS a, products AS b\
                                    WHERE a.movieid  = b.movieid AND b.prod_id = "+id+"")

        db_conn.close()
        return list(db_result)[0][0]
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)
        return False


def eliminarFilm(id, username):
    """Funcion que elimina una pelicula del carrito de un usuario

    Args:
        id (string): Id del producto a eliminar
        username (string): Username del customer al que hay que modificar el carrito

    Return:
        True en caso de exito, False en caso de error
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtenemos el carrito
        db_result = db_conn.execute("SELECT orderid\
                                    FROM orders AS a, customers AS b\
                                    WHERE b.customerid = a.customerid AND b.username = '"+username+"' AND a.status IS NULL")
        orderid_carrito = list(db_result)[0][0]

        # Comprobamos cuantas peliculas hay
        db_result = db_conn.execute("SELECT quantity\
                                    FROM orders AS a, orderdetail AS b\
                                    WHERE a.orderid = b.orderid AND a.orderid = "+orderid_carrito+" AND b.prod_id = "+id+"")
        quantity = list(db_result)[0][0]

        if quantity > 1:
            # Si hay más de una solo reducimos la cantidad
            db_conn.execute("UPDATE orderdetail\
                            SET quantity = quantity - 1\
                            WHERE orderid = "+orderid_carrito+" AND prod_id = "+id+"")
        else:
            # Si solo hay una eliminamos la fila
            db_conn.execute("DELETE FROM orderdetail WHERE orderid = "+orderid_carrito+" AND prod_id = "+id+"")

        db_conn.close()
        return True
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)
        return False


def carritoFilms(username):
    """Función que devuelve el carrito en una lista

    Args:
        username (string): Username del que hay que coger el carrito
    """
    try:
        # conexion a la base de datos
        db_conn = None
        db_conn = db_engine.connect()

        # Obtenemos el carrito
        db_result = db_conn.execute("SELECT orderid\
                                    FROM orders AS a, customers AS b\
                                    WHERE b.customerid = a.customerid AND b.username = '"+username+"' AND a.status IS NULL")
        orderid_carrito = list(db_result)[0][0]

        
        db_conn.close()
        return True
    except:
        if db_conn is not None:
            db_conn.close()
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)
        return False
