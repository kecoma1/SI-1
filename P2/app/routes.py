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

# Catálogo
catalogue = None
catalogue_data = open(os.path.join(
    app.root_path, 'catalogue/catalogue.json')).read()
catalogue = json.loads(catalogue_data)

# Variables para guardar el usuario logeado
loaded_posters = False

# Stack donde guardamos las urls visitadas
stack_url = deque()

def goBack():
    """
        Función para volver a la página anterior

        Return:
            Nos redirige a la página anterior
    """
    global stack_url
    stack_url.pop()
    return redirect(stack_url[0])

def stack_push(url):
    """
        Guarda en la stack la dirección actual
    """
    global stack_url
    stack_url.append(url)


def cargar_films():
    """
        Función que carga las peliculas en una lista usada en el carrito 
    """
    global catalogue
    carrito_films = []
    for film in catalogue['peliculas']:
        if str(film['id']) in session:
            i = 0
            while i < session[str(film['id'])]:
                carrito_films.append(film)
                i += 1
    return carrito_films


def logged():
    """
        Función para comprobar si alguien ha hecho login 
    """
    if 'usuario' in session:
        return True
    else:
        return False


@app.route('/')
@app.route('/index')
def index():
    global catalogue
    top_films = database.db_top_films()
    if top_films == False:
        return
    stack_push(request.url)
    return render_template('index.html', movies=top_films, logged=logged())


@app.route('/back')
def back():
    global stack_url
    stack_url.pop()
    if len(stack_url) != 0:
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
            return redirect(url_for('index'))
        else:
            return render_template('login.htailml', title='login', logged=logged(), error="El usuario o la contrasenha son incorrectos")
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
        return redirect(url_for('index'))
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

        income = request.form['income']
        if income == '':
            income = 'null'
        
        gender = request.form['gender']
        if gender == '':
            gender = 'null'
        else:
            gender = "'"+gender[:1]+"'"
        

        creditcard = creditcard.replace(' ', '')
        # TODO Comprobar si hay cartera o no, wallet = random.randrange(0, 100)

        if database.registrar(firstname, lastname, address1, address2, 
                           city, state, zipcode, country, region, email, 
                           phone, creditcardType, creditcard, creditcardexpiration, 
                           username, password, age, income, gender) == False:
            return render_template('signup.html', title='signup', logged=logged(), error="Ya existe ese usurname o hubo un error")
        else:
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


@app.route("/historial.html", methods=['GET'])
def historial():
    return redirect(url_for('index'))
    if logged():
        #TODO implementar esto con los triggers
        # Cargando el archivo del usuario
        dir_path = homedir = os.path.expanduser("~")
        dir_path += "/public_html/usuarios/"+session['usuario']
        f = open(dir_path+"/datos.dat", "r")
        data = f.read()
        f.close()
        data = data.split(' ')
        saldo = data[4]
        f.close()

        f = open(dir_path+"/historial.json", "r")
        if f is not None:
            historial_data = f.read()
            if historial_data != '':
                historial = json.loads(historial_data)
            else:
                historial = []
            f.close()
        stack_push(request.url)
        return render_template('historial.html', logged=logged(), saldo=saldo, historial=historial)
    else:
        return redirect(url_for('index'))


@app.route("/carrito.html", methods=['GET', 'POST'])
def carrito():
    global catalogue
    carrito_films = []
    if request.method == 'GET':
        for film in catalogue['peliculas']:
            if str(film['id']) in session:
                i = 0
                while i < session[str(film['id'])]:
                    carrito_films.append(film)
                    i += 1
        stack_push(request.url)
        return render_template('carrito.html', logged=logged(), carrito_films=carrito_films)
    else:
        pass
    return redirect(url_for('carrito'))


@app.route("/index/<id>", methods=['GET'])
def film_detail(id):
    global catalogue
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
    global catalogue
    peliculas_categoria = database.categoria(categoria)
    if peliculas_categoria == False:
        return redirect(url_for('index'))
    stack_push(request.url)
    return render_template('category.html', movies=peliculas_categoria, categoria=categoria)


@app.route("/busqueda", methods=['POST'])
def busqueda():
    global catalogue
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


@app.route("/cargar_categoria/carrito.html", methods=['GET'])
@app.route("/realizar_compra/carrito.html", methods=['GET'])
@app.route("/index/carrito.html", methods=['GET'])
def redirect_carrito():
    stack_push(request.url)
    return redirect(url_for('carrito'))


# Rutas para el carrito
@app.route("/index/anhadir_carrito/<string:id>", methods=['POST'])
def anhadir_carrito(id):
    if id in session:
        session[id] += 1
    else:
        session[id] = 1
    return redirect(url_for('film_detail', id=id))


@app.route("/realizar_compra/eliminar_carrito/<string:id>", methods=['POST'])
@app.route("/eliminar_carrito/<string:id>", methods=['POST'])
def eliminar_carrito(id):
    if id in session:
        session[id] -= 1

    if session[id] == 0:
        session.pop(id, None)
    return redirect(url_for('carrito'))

@app.route("/comprar_todo", methods=['POST'])
def comprar_todo():
    global catalogue
    precio = 0
    lista_pelis = []
    if logged():
        # Cargando el archivo del usuario
        dir_path = homedir = os.path.expanduser("~")
        dir_path += "/public_html/usuarios/"+session['usuario']
        f = open(dir_path+"/datos.dat", "r+")
        data = f.read()
        data = data.split(' ')
        saldo = float(data[4])

        if logged() == True:
            # Buscamos las peliculas del carrito
            for film in catalogue['peliculas']:

                # Si la pelicula esta en el carrito calcular precio total
                if str(film['id']) in session:
                    precio += film['precio']*int(session[str(film['id'])])
                    lista_pelis.append(film)

            # Comprobamos si hay saldo suficiente
            if saldo > precio:

                # Eliminando información anterior del archivo
                f.seek(0)
                f.truncate()

                f.write(data[0]+" "+data[1]+" " +
                        data[2]+" "+data[3]+" "+str(saldo))
                f.close()
                f = open(dir_path+"/historial.json", "r+")
                historial_data = f.read()

                if historial_data != '':
                    historial = json.loads(historial_data)
                else:
                    historial = []

                now = datetime.datetime.now()
                for film in lista_pelis:
                    historial.append(film)
                    historial[-1]['time'] = now.strftime(
                        "%Y-%m-%d %H:%M:%S")
                    historial[len(historial)-1]['movement_id'] = len(historial)
                    historial[len(historial)-1]['quantity'] = session[str(film['id'])]
                
                f.seek(0)
                f.truncate()
                json.dump(historial, f)
                f.close()

                for pelicula in lista_pelis:
                    if str(pelicula['id']) in session:
                        session.pop(str(pelicula['id']), None)
                    else:
                        pass

                carrito_films = cargar_films()
            
                return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, error="Compra realizada con exito")

            else:
                carrito_films = cargar_films()
            
                return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, error="No hay suficiente saldo")

    carrito_films = cargar_films()

    return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, error="Haga login para comprar")


@app.route("/realizar_compra/<string:id>", methods=['POST', 'GET'])
def realizar_compra(id):
    global catalogue
    if logged():
        # Cargando el archivo del usuario
        dir_path = homedir = os.path.expanduser("~")
        dir_path += "/public_html/usuarios/"+session['usuario']
        f = open(dir_path+"/datos.dat", "r+")
        data = f.read()
        data = data.split(' ')
        saldo = float(data[4])

        if logged() == True:
            for film in catalogue['peliculas']:
                if id in session and str(film['id']) == id:
                    if saldo > float(film['precio']):
                        saldo = saldo - film['precio']

                        # Eliminando información anterior del archivo
                        f.seek(0)
                        f.truncate()

                        f.write(data[0]+" "+data[1]+" " +
                                data[2]+" "+data[3]+" "+str(saldo))
                        f.close()
                        f = open(dir_path+"/historial.json", "r+")
                        historial_data = f.read()

                        if historial_data != '':
                            historial = json.loads(historial_data)
                        else:
                            historial = []

                        historial.append(film)
                        now = datetime.datetime.now()
                        historial[-1]['time'] = now.strftime(
                            "%Y-%m-%d %H:%M:%S")
                        historial[-1]['movement_id'] = len(historial)
                        historial[len(historial)-1]['quantity'] = 1
                        f.seek(0)
                        f.truncate()
                        json.dump(historial, f)
                        f.close()

                        if str(film['id']) in session:
                            session[str(film['id'])] -= 1
                            if session[str(film['id'])] == 0:
                                session.pop(str(film['id']), None)
                            else:
                                pass

                        carrito_films = cargar_films()
                    
                        return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, error="Compra realizada con exito")

                    else:
                        carrito_films = cargar_films()
                    
                        return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, error="No hay suficiente saldo")

    carrito_films = cargar_films()

    return render_template('carrito.html', logged=logged(), carrito_films=carrito_films, error="Haga login para comprar")


@app.route("/index/cargar_categoria/<string:categoria>", methods=['GET'])
@app.route("/cargar_categoria/cargar_categoria/<string:categoria>", methods=['GET'])
@app.route("/realizar_compra/cargar_categoria/<string:categoria>", methods=['POST'])
def redirect_category(categoria):
    stack_push(request.url)
    return redirect(url_for('category', categoria=categoria))


@app.route("/index/busqueda", methods=['POST'])
def redirect_busqueda():
    global catalogue
    busqueda = request.form['search']
    peliculas = []
    for film in catalogue['peliculas']:
        if busqueda in film['titulo']:
            peliculas.append(film)
    stack_push(request.url)
    return redirect(url_for('busqueda', movies=peliculas))


@app.route("/realizar_compra/realizar_compra/<string:id>", methods=['POST'])
def redirect_realizar_compra(id):
    return redirect(url_for('realizar_compra', id=id))


@app.route("/introducir_saldo", methods=['POST'])
def introducir_saldo():
    if logged():
        saldo_a_introducir = request.form['input_saldo']
        dir_path = homedir = os.path.expanduser("~")
        dir_path += "/public_html/usuarios/"+session['usuario']
        f = open(dir_path+"/datos.dat", "r+")
        data = f.read()
        data = data.split(' ')
        saldo = data[4]
        saldo_actual = float(saldo)
        saldo = float(saldo_a_introducir)+float(saldo_actual)

        f.seek(0)
        f.truncate()

        f.write(data[0]+" "+data[1]+" "+data[2]+" "+data[3]+" "+str(saldo))
        f.close()
        return redirect(url_for('historial'))
    else:
        return redirect(url_for('index'))
