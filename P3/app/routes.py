#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from app import database
from flask import render_template, request, url_for, redirect, session
from collections import deque
import json
import os
import sys
import hashlib
import random
import datetime
import pymongo

# Base de datos mongodb
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["si1"]
mycol = mydb["topUSA"]

# Stack donde guardamos las urls visitadas
stack_url = deque()

def stack_push(url):
    """Guarda en la stack la dirección actual

    Args:
        url (string): URL de la página actual
    """
    global stack_url
    stack_url.append(url)


def logged():
    """Función para comprobar si alguien ha hecho login 

    Returns:
        Bool: True si ha hecho login, False si no
    """
    if 'usuario' in session:
        return True
    else:
        return False


def getSessionNetoCarrito(carrito):
    """Función que calcula el total de la compra dada la sesión con el carrito

    Args:
        Carrito (list): Lista con las ids de cada producto en el carrito

    Returns:
        float: Precio total
    """
    precio = 0.0
    for film in carrito:
        precio += float(database.getPrice(film))
    return precio

@app.route('/')
@app.route('/index')
def index():
    top_films = [[442893, 'Wizard of Oz, The (1939)', '', 0, '1939', 0], 
                 [229764, 'Life Less Ordinary, A (1997)', '', 0, '1997', 0],
                 [149475, 'Gang Related (1997)', '', 0, '1997', 0]]
    #top_films = database.db_top_films()
    if top_films == False:
        return
    stack_push(request.url)
    return render_template('index.html', movies=top_films, logged=logged())


@app.route('/back')
def back():
    """
        Función para volver a la página anterior

        Return:
            Nos redirige a la página anterior
    """
    global stack_url
    if len(stack_url) != 0:
        stack_url.pop()
        return redirect(stack_url.pop())
    else:
        return redirect(url_for('index'))

# Rutas a las diferentes páginas
@app.route("/sidenav.html", methods=['GET'])
def sidenav():
    return render_template('sidenav.html', logged=logged())


@app.route("/topnav.html", methods=['GET'])
def topnav():
    return render_template('topnav.html', logged=logged())


@app.route("/login.html", methods=['POST'])
def login_page_POST():
    if request.form['username']:
        username = request.form['username']
        password = request.form['password']

        # Comprobamos si existe el usuario
        if database.validar(username, password) == True:
            session.permanent = False
            session['usuario'] = username

            if 'carrito' in session:    
                if database.addSessionToCarrito(session['carrito'], username) == False:
                    print("Error anadiendo las películas de la sesión a la BD")
                session.pop('carrito', None)

            return redirect(url_for('index'))
        else:
            return render_template('login.html', title='login', logged=logged(), error="El usuario o la contrasenha son incorrectos")
    else:
        return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

@app.route("/login.html", methods=['GET'])
def login_page_GET():
    if logged():
        # Cerrando sesión
        if 'usuario' in session:
            session.pop('usuario', None)

        # Eliminando el carrito de la sesión
        for id in session:
            if id != 'usuario':
                session[id] = 0
        return redirect(url_for('login_page_GET'))
    else:
        stack_push(request.url)
        return render_template('login.html', title='login', logged=logged())


@app.route("/signup.html", methods=['POST'])
def signup_page():
    if logged() == True:
        return render_template('signup.html', title='signup', logged=logged(), error="Cierre sesion por favor")

    if request.form['username']:
        firstname = request.form['firstname']
        if len(firstname) > 50: # Comprobamos que los campos no tengan + de 50 caracteres
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        lastname = request.form['lastname']
        if len(lastname) > 50:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        # Los campos que pueden ser null y no tienen información, los cambiamos
        address1 = request.form['direccion1']
        if address1 == '':
            address1 = 'null'
        else:
            address1 = "'"+address1+"'"
        if len(address1) > 52: # Tenemos en cuenta las comillas
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")
            
        address2 = request.form['direccion2']
        if address2 == '':
            address2 = 'null' 
        else:
            address2 = "'"+address2+"'"
        if len(address2) > 52:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        city = request.form['city']
        if len(city) > 50:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        state = request.form['state']
        if state == '':
            state = 'null'
        else:
            state = "'"+state+"'"
        if len(state) > 52:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        zipcode = request.form['zipcode']
        if len(zipcode) > 9:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        country = request.form['country']
        if len(country) > 50:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        region = request.form['region']
        if len(region) > 6:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        email = request.form['email']
        if email == '':
            email = 'null'
        else:
            email = "'"+email+"'"
        if len(email) > 50:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        phone = request.form['phone']
        if phone == '':
            phone = 'null'
        else:
            phone = "'"+phone+"'"
        if len(phone) > 52:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        creditcardType = request.form['creditcardtype']
        if len(creditcardType) > 50:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        creditcard = request.form['card']
        if len(creditcard) > 50:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        creditcardexpiration = request.form['creditcardexpiration']
        if len(creditcardexpiration) > 50:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        username = request.form['username']
        if len(username) > 50:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        password = request.form['password_input']
        if len(password) > 50:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")

        age = request.form['age']
        if age == '':
            age = 'null'
        if len(age) > 50:
            return render_template('signup.html', title='signup', logged=logged(), error="Los datos no fueron introducidos correctamente")
        
        gender = request.form['gender']
        if gender == '':
            gender = 'null'
        else:
            gender = "'"+gender[:1]+"'"
        

        creditcard = creditcard.replace(' ', '')

        if database.registrar(firstname, lastname, address1, address2, 
                           city, state, zipcode, country, region, email, 
                           phone, creditcardType, creditcard, creditcardexpiration, 
                           username, password, age, gender) == False:
            session.permanent = False
            session['usuario'] = username

            return render_template('signup.html', title='signup', logged=logged(), error="Ya existe ese usurname o hubo un error")
        else:
            if 'carrito' in session:    
                if database.addSessionToCarrito(session['carrito'], username) == False:
                    print("Error anadiendo las películas de la sesión a la BD")
                session.pop('carrito', None)

            session.permanent = False
            session['usuario'] = username
            return redirect(url_for('index'))


@app.route("/signup.html", methods=['GET'])
def signup_page_get():
    if logged() == True:
        stack_push(request.url)
        return render_template('signup.html', title='signup', logged=logged(), error="Cierre sesión por favor")
    else:   
        stack_push(request.url)
        return render_template('signup.html', title='signup', logged=logged())


@app.route("/topUSA.html", methods=['GET'])
def topUSA():
    global mycol
    
    # Comedias de 1997 con "Life" en el titulo
    first_table = mycol.find({'$and': 
                                [
                                    {"year":'1997'}, 
                                    {"genres":{'$elemMatch': {'$regex' : ".*Comedy.*"}}},
                                    {"title": {'$regex': ".*Life.*"}}
                                ]
                            })

    # Peliculas dirigidas por Woody Allen en los 90
    second_table = mycol.find({'$and': 
                                [
                                    {'year': {'$lt':'2000'}}, 
                                    {'year':{'$gt': '1989'}}, 
                                    {'directors': {'$elemMatch': {'$regex': '.*Woody.*'}}},
                                    {'directors': {'$elemMatch': {'$regex': '.*Allen.*'}}}
                                ]
                            })

    # Peliculas en las que Johnny Galecki y Jim Parsons compartan reparto
    third_table = mycol.find({"$and": 
                                [
                                    {"actors": {'$elemMatch': {'$regex': ".*Parsons, Jim.*"}}}, 
                                    {"actors": {'$elemMatch': {'$regex': ".*Galecki, Johnny.*"}}}
                                ]
                            })
    return render_template('topUSA.html', logged=logged(), first_table=list(first_table), second_table=list(second_table), third_table=list(third_table))

@app.route("/historial.html", methods=['GET'])
def historial():
    if logged():
        username = session['usuario']
        # Obtenemos el saldo -> getSaldo(username)
        saldo = database.getSaldo(username)
        # Obtenemos las orders así [order -> 1, mov..., detail -> [[1, mov, ...] [2, ...]]
        historial = database.getHistorial(username)
        if historial == False:
            print("Error al obtener el historial")
            return redirect(url_for('login_page_GET'))
        
        return render_template('historial.html', logged=logged(), saldo=saldo, historial=historial)
    else:
        return redirect(url_for('login_page_GET'))


@app.route("/carrito.html", methods=['GET'])
def carrito():
    total = 0
    neto = 0
    if logged():
        carrito_films = database.carritoFilms(session['usuario'])
        if carrito_films == False:
            carrito_films = []
            total = 0
            neto = 0
        else:
            total = database.getTotalCarrito(session['usuario'])
            neto = database.getNetoCarrito(session['usuario'])
    else:
        if 'carrito' in session:
            if session['carrito'] != 0:
                carrito_films = database.carritoFilmsFromSession(session['carrito'])
                neto = getSessionNetoCarrito(session['carrito'])
                total = 0 # Como no sabémos el tax no podemos calcular el total
            else: 
                carrito_films = []
            return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, total=float(round(total, 2)),  total2=float(round(neto, 2)), error="TAX no aplicado")
        else:
            carrito_films = []
    stack_push(request.url)
    return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, total=float(round(total, 2)), total2=float(round(neto, 2)))


@app.route("/index/<id>", methods=['GET'])
def film_detail(id):
    pelicula = database.getPelicula(id)
    if pelicula == False:
        print("Error cogiendo la película")
        return redirect(url_for('index'))

    actores = database.getActores(id)
    if actores == False:
        print("Error cogiendo los actores")
        return redirect(url_for('index'))

    directores = database.getDirectores(id)
    if directores == False:
        print("Error cogiendo los precios")
        return redirect(url_for('index'))

    precios = database.getPrecio(id)
    if precios == False:
        print("Error cogiendo los precios")
        return redirect(url_for('index'))
    stack_push(request.url)
    return render_template('filmDetail.html', film=pelicula, actores=actores, directores=directores, precios=precios, logged=logged())


@app.route("/cargar_categoria/<string:categoria>", methods=['GET'])
def category(categoria):
    peliculas_categoria = database.categoria(categoria)
    if peliculas_categoria == False:
        return redirect(url_for('index'))
    stack_push(request.url)
    return render_template('category.html', movies=peliculas_categoria, categoria=categoria)


@app.route("/busqueda", methods=['POST'])
def busqueda():
    busqueda = request.form['search']

    # Buscamos la pelicula en la base de datos
    peliculas = database.buscarPeliculas(busqueda)
    if peliculas == False:
        return redirect(url_for('index'))
    stack_push(request.url)
    return render_template('busqueda.html', movies=peliculas)


# Redirects desde index/<id>
@app.route("/index.html", methods=['GET', 'POST'])
@app.route("/index/index", methods=['GET'])
@app.route("/cargar_categoria/index", methods=['GET'])
@app.route("/realizar_compra/index", methods=['GET'])
def redirect_index():
    stack_push(request.url)
    return redirect(url_for('index'))


@app.route("/realizar_compra/index/<id>", methods=['GET'])
@app.route("/cargar_categoria/index/<id>", methods=['GET'])
def redirect_filmDetail(id):
    return redirect(url_for('film_detail', id=id))


@app.route("/cargar_categoria/login.html", methods=['GET'])
@app.route("/realizar_compra/login.html", methods=['GET'])
@app.route("/index/login.html", methods=['GET'])
def redirect_login_page():
    stack_push(request.url)
    return redirect(url_for('login_page_GET'))


@app.route("/cargar_categoria/signup.html", methods=['GET'])
@app.route("/realizar_compra/signup.html", methods=['GET'])
@app.route("/index/signup.html", methods=['GET'])
def redirect_signup_page():
    return redirect(url_for('signup_page_get'))


@app.route("/realizar_compra/topnav.html", methods=['GET'])
@app.route("/cargar_categoria/topnav.html", methods=['GET'])
@app.route("/index/topnav.html", methods=['GET'])
def redirect_topnav():
    return render_template('topnav.html', logged=logged())


@app.route("/realizar_compra/sidenav.html", methods=['GET'])
@app.route("/cargar_categoria/sidenav.html", methods=['GET'])
@app.route("/index/sidenav.html", methods=['GET'])
def redirect_sidenav():
    return render_template('sidenav.html', logged=logged())


@app.route("/cargar_categoria/historial.html", methods=['GET'])
@app.route("/realizar_compra/historial.html", methods=['GET'])
@app.route("/index/historial.html", methods=['GET'])
def redirect_historial():
    stack_push(request.url)
    return redirect(url_for('historial'))


@app.route("/cargar_categoria/topUSA.html", methods=['GET'])
@app.route("/realizar_compra/topUSA.html", methods=['GET'])
@app.route("/index/topUSA.html", methods=['GET'])
def redirect_topUSA():
    stack_push(request.url)
    return redirect(url_for('topUSA'))


@app.route("/cargar_categoria/carrito.html", methods=['GET'])
@app.route("/realizar_compra/carrito.html", methods=['GET'])
@app.route("/index/carrito.html", methods=['GET'])
def redirect_carrito():
    stack_push(request.url)
    return redirect(url_for('carrito'))


# Rutas para el carrito
@app.route("/index/anhadir_carrito/<string:id>", methods=['POST'])
def anhadir_carrito(id):
    # Comprobamos si es usuario ha hecho login
    if logged() == False:
        # Usamos sesiones en caso de no haberse hecho login
        if 'carrito' in session:
            if session['carrito'] == 0:
                session['carrito'] = []
                session['carrito'].append(id)
            else:
                session['carrito'].append(id)
        else:
            session['carrito'] = []
            session['carrito'].append(id)
        return redirect(url_for('film_detail', id=database.getMovieId(id)))
    else:
        # Usamos la base de datos al estar logeado
        movieid = database.anadirFilm(id, session['usuario'])
        if movieid == False:
            print("Error anadiendo la pelicula")
            return redirect(url_for('index'))
        return redirect(url_for('film_detail', id=movieid))


@app.route("/realizar_compra/eliminar_carrito/<string:id>", methods=['POST'])
@app.route("/eliminar_carrito/<string:id>", methods=['POST'])
def eliminar_carrito(id):
    # Comprobamos si es usuario ha hecho login
    if logged() == False:
        # Usamos sesiones en caso de no haberse hecho login
        session['carrito'].remove(id)
    else:
        # Usamos la base de datos al estar logeado
        if database.eliminarFilm(id, session['usuario']) == False:
            print("Error eliminando la pelicula")
            return redirect(url_for('index'))
    return redirect(url_for('carrito'))


@app.route("/comprar_todo", methods=['POST', 'GET'])
def comprar_todo():
    if logged():
        if database.comprarTodo(session['usuario']) == False:
            carrito_films = database.carritoFilms(session['usuario'])
            if carrito_films == False:
                return redirect(url_for('carrito'))
                
            total = database.getTotalCarrito(session['usuario'])
            neto = database.getNetoCarrito(session['usuario'])
            return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, total=float(round(total, 2)),  total2=float(round(neto, 2)), error="ERROR, consulte su saldo")
        else:
            carrito_films = []
            total = 0
            neto = 0
            return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, total=float(round(total, 2)),  total2=float(round(neto, 2)), error="Compra realizada con exito")
    else:
        carrito_films = database.carritoFilmsFromSession(session['carrito'])
        if carrito_films == False:
                return redirect(url_for('carrito'))
                
        neto = getSessionNetoCarrito(session['carrito'])
        total = 0
        return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, total=float(round(total, 2)),  total2=float(round(neto, 2)), error="Haga login para comprar")


@app.route("/realizar_compra/<string:id>", methods=['POST', 'GET'])
def realizar_compra(id):
    if logged():
        if database.comprarUnidad(id, session['usuario']) == False:
            carrito_films = database.carritoFilms(session['usuario'])
            if carrito_films == False:
                return redirect(url_for('carrito'))
                
            total = database.getTotalCarrito(session['usuario'])
            neto = database.getNetoCarrito(session['usuario'])
            return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, total=float(round(total, 2)),  total2=float(round(neto, 2)), error="ERROR, consulte su saldo")
        else:
            carrito_films = database.carritoFilms(session['usuario'])
            if carrito_films == False:
                return redirect(url_for('carrito'))
                
            total = database.getTotalCarrito(session['usuario'])
            neto = database.getNetoCarrito(session['usuario'])
            return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, total=float(round(total, 2)),  total2=float(round(neto, 2)), error="Compra realizada con éxito")
    else:
        carrito_films = database.carritoFilmsFromSession(session['carrito'])
        if carrito_films == False:
                return redirect(url_for('carrito'))

        neto = getSessionNetoCarrito(session['carrito'])
        total = 0
        return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, total=float(round(total, 2)),  total2=float(round(neto, 2)), error="Haga login para comprar")


@app.route("/index/cargar_categoria/<string:categoria>", methods=['GET'])
@app.route("/cargar_categoria/cargar_categoria/<string:categoria>", methods=['GET'])
@app.route("/realizar_compra/cargar_categoria/<string:categoria>", methods=['POST'])
def redirect_category(categoria):
    stack_push(request.url)
    return redirect(url_for('category', categoria=categoria))


@app.route("/index/busqueda", methods=['POST'])
def redirect_busqueda():
    # Buscamos la pelicula en la base de datos
    busqueda = request.form['search']
    peliculas = database.buscarPeliculas(busqueda)
    if peliculas == False:
        return redirect(url_for('index'))
    stack_push(request.url)
    return redirect(url_for('busqueda', movies=peliculas))


@app.route("/realizar_compra/realizar_compra/<string:id>", methods=['POST'])
def redirect_realizar_compra(id):
    return redirect(url_for('realizar_compra', id=id))


@app.route("/realizar_compra/comprar_todo", methods=['POST'])
def redirect_comprar_todo():
    return redirect(url_for('comprar_todo'))

@app.route("/introducir_saldo", methods=['POST'])
def introducir_saldo():
    if logged():
        saldo_a_introducir = request.form['input_saldo']
        if database.introducir_saldo(session['usuario'], saldo_a_introducir) == False:
            print("Error al introducir el saldo")
            return redirect(url_for('historial'))
        else:
            return redirect(url_for('historial'))
    else:
        return redirect(url_for('login_page_GET'))


