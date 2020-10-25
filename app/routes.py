#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
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
logged = False
username_logged = None


@app.route('/')
@app.route('/index')
def index():
    global catalogue, logged
    return render_template('index.html', movies=catalogue['peliculas'], logged=logged)

# Rutas a las diferentes páginas


@app.route("/sidenav.html", methods=['GET'])
def sidenav():
    global logged
    return render_template('sidenav.html', logged=logged)


@app.route("/topnav.html", methods=['GET'])
def topnav():
    global logged
    return render_template('topnav.html', logged=logged)


@app.route("/bottonnav.html", methods=['GET'])
def bottonnav():
    return render_template('bottonnav.html')


@app.route("/login.html", methods=['POST'])
def login_page_POST():
    global logged, username_logged
    if request.form['username']:
        username = request.form['username']
        password = hashlib.sha512(
            (request.form['password']).encode('utf-8')).hexdigest()

        # Comprobamos si existe el usuario
        dir_path = homedir = os.path.expanduser("~")
        dir_path += "/public_html/usuarios/"+username
        if os.path.exists(dir_path):
            f = open(dir_path+"/datos.dat", "r")
            data = f.read()
            f.close()
            data = data.split(' ')
            users_password = data[1]
            if users_password == password:
                session.permanent = False
                session['usuario'] = username
                logged = True
                username_logged = username
                return redirect(url_for('index'))
            else:
                return render_template('login.html', title='login', logged=logged, error="El usuario o contraseña incorrectos")
        else:
            return render_template('login.html', title='login', logged=logged, error="El usuario o contraseña incorrectos")
    else:
        return render_template('signup.html', title='signup', logged=logged, error="Los datos no fueron introducidos correctamente")


@app.route("/login.html", methods=['GET'])
def login_page_GET():
    global logged
    if logged:
        # Cerrando sesión
        logged = False
        username_logged = None
        if 'usuario' in session:
            session.pop('usuario', None)
        
        #Eliminando el carrito de la sesión
        for id in session:
            if id != 'usuario':
                session[id] = 0
        return redirect(url_for('index'))
    else:
        return render_template('login.html', title='login', logged=logged)


@app.route("/signup.html", methods=['POST'])
def signup_page():
    global logged, username_logged
    if logged == True:
        return render_template('signup.html', title='signup', logged=logged, error="Cierre sesión por favor")

    if request.form['username']:
        username = request.form['username']
        password = hashlib.sha512(
            (request.form['password_input']).encode('utf-8')).hexdigest()
        card = request.form['card']
        card = card.replace(' ', '')
        wallet = random.randrange(0, 100)

        session.permanent = False
        session['usuario'] = username

        # Comprobamos si existe el usuario
        dir_path = homedir = os.path.expanduser("~")
        dir_path += "/public_html/usuarios/"+username
        if os.path.exists(dir_path):
            return render_template('signup.html', title='signup', logged=logged, error="El usuario ya existe")
        else:
            os.mkdir(dir_path)

            # Creando historial
            f = open(dir_path+"/historial.json", "w")
            f.close()

            # Escribiendo los datos
            f = open(dir_path+"/datos.dat", "w")
            f.write(username+" "+password+" " +
                    request.form['email']+" "+card+" "+str(wallet))
            f.close()

            logged = True
            username_logged = username
            return redirect(url_for('index'))
    else:
        return render_template('signup.html', title='signup', logged=logged, error="Los datos no fueron introducidos correctamente")


@app.route("/signup.html", methods=['GET'])
def signup_page_get():
    global logged
    if logged == True:
        return render_template('signup.html', title='signup', logged=logged, error="Cierre sesión por favor")
    else:
        return render_template('signup.html', title='signup', logged=logged)


@app.route("/historial.html", methods=['GET'])
def historial():
    global logged, username_logged

    if logged:
        # Cargando el archivo del usuario
        dir_path = homedir = os.path.expanduser("~")
        dir_path += "/public_html/usuarios/"+username_logged
        f = open(dir_path+"/datos.dat", "r")
        data = f.read()
        f.close()
        data = data.split(' ')
        saldo = data[4]
        f.close()
        
        f = open(dir_path+"/historial.json", "r")
        historial_data = f.read()
        if historial_data != '':
            historial = json.loads(historial_data)
        else:
            historial = []
        return render_template('historial.html', logged=logged, saldo=saldo, historial=historial)
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
        return render_template('carrito.html', logged=logged, carrito_films=carrito_films)
    else:
        pass
    return redirect(url_for('carrito'))


@app.route("/index/<id>", methods=['GET'])
def film_detail(id):
    global catalogue, logged
    return render_template('filmDetail.html', film=catalogue['peliculas'][int(id)-1], logged=logged)

@app.route("/cargar_categoria/<string:categoria>", methods=['GET'])
def category(categoria):
    global catalogue
    return render_template('category.html', movies=catalogue['peliculas'], categoria=categoria)

@app.route("/busqueda", methods=['POST'])
def busqueda():
    global catalogue
    busqueda = request.form['search']
    peliculas = []
    for film in catalogue['peliculas']:
        if busqueda in film['titulo']:
            peliculas.append(film)
    return render_template('busqueda.html', movies=peliculas)

# Redirects desde index/<id>

@app.route("/index.html", methods=['GET', 'POST'])
@app.route("/index/index", methods=['GET'])
@app.route("/cargar_categoria/index", methods=['GET'])
@app.route("/realizar_compra/index", methods=['GET'])
def redirect_index():
    return redirect(url_for('index'))

@app.route("/realizar_compra/index/<id>", methods=['GET'])
@app.route("/cargar_categoria/index/<id>", methods=['GET'])
def redirect_filmDetail(id):
    return redirect(url_for('film_detail', id= id))

@app.route("/realizar_compra/login.html", methods=['GET'])
@app.route("/index/login.html", methods=['GET'])
def redirect_login_page():
    return redirect(url_for('login_page_GET'))

@app.route("/realizar_compra/signup.html", methods=['GET'])
@app.route("/index/signup.html", methods=['GET'])
def redirect_signup_page():
    return redirect(url_for('signup_page_get'))

@app.route("/realizar_compra/topnav.html", methods=['GET'])
@app.route("/cargar_categoria/topnav.html", methods=['GET'])
@app.route("/index/topnav.html", methods=['GET'])
def redirect_topnav():
    return render_template('topnav.html', logged=logged)

@app.route("/realizar_compra/sidenav.html", methods=['GET'])
@app.route("/cargar_categoria/sidenav.html", methods=['GET'])
@app.route("/index/sidenav.html", methods=['GET'])
def redirect_sidenav():
    return render_template('sidenav.html', logged=logged)

@app.route("/realizar_compra/historial.html", methods=['GET'])
@app.route("/index/historial.html", methods=['GET'])
def redirect_historial():
    return redirect(url_for('historial'))

@app.route("/realizar_compra/carrito.html", methods=['GET'])
@app.route("/index/carrito.html", methods=['GET'])
def redirect_carrito():
    return redirect(url_for('carrito'))

# Rutas para el carrito

@app.route("/index/añadir_carrito/<string:id>", methods=['POST'])
def añadir_carrito(id):
    if id in session:
        session[id] += 1
    else:
        session[id] = 1
    return redirect(url_for('film_detail', id=id))


@app.route("/eliminar_carrito/<string:id>", methods=['POST'])
def eliminar_carrito(id):
    if id in session:
        session[id] -= 1

    if session[id] == 0:
        session.pop(id, None)
    return redirect(url_for('carrito'))


@app.route("/realizar_compra/<string:id>", methods=['POST', 'GET'])
def realizar_compra(id):
    global catalogue, username_logged
    if logged:
        # Cargando el archivo del usuario
        dir_path = homedir = os.path.expanduser("~")
        dir_path += "/public_html/usuarios/"+username_logged
        f = open(dir_path+"/datos.dat", "r+")
        data = f.read()
        data = data.split(' ')
        saldo = float(data[4])

        if logged == True:
            for film in catalogue['peliculas']:
                if id in session and str(film['id']) == id:
                    if saldo > float(film['precio']):
                        saldo = saldo - film['precio']
                        
                        # Eliminando información anterior del archivo
                        f.seek(0)  
                        f.truncate()  

                        f.write(data[0]+" "+data[1]+" " +data[2]+" "+data[3]+" "+str(saldo))
                        f.close()
                        f = open(dir_path+"/historial.json", "r+")
                        historial_data = f.read()

                        if historial_data != '':
                            historial = json.loads(historial_data)
                        else:
                            historial = []
                       
                        historial.append(film)
                        now = datetime.datetime.now()
                        historial[-1]['time'] = now.strftime("%Y-%m-%d %H:%M:%S")
                        if len(historial) > 1:
                            movement_id = historial[-2]['movement_id']+1
                            historial[-1]['movement_id'] = movement_id
                        else:
                            historial[-1]['movement_id'] = 1
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
                        return render_template('carrito.html', logged=logged, carrito_films=carrito_films, error="Compra realizada con exito")
                        
                    else:
                        carrito_films = cargar_films()
                        return render_template('carrito.html', logged=logged, carrito_films=carrito_films, error="No hay suficiente saldo")
    
    carrito_films = cargar_films()
    return render_template('carrito.html', logged=logged, carrito_films=carrito_films, error="Haga login para comprar")

def cargar_films():
    global catalogue
    carrito_films = []
    for film in catalogue['peliculas']:
        if str(film['id']) in session:
            i = 0
            while i < session[str(film['id'])]:
                carrito_films.append(film)
                i += 1
    return carrito_films

@app.route("/index/cargar_categoria/<string:categoria>", methods=['GET'])
@app.route("/cargar_categoria/cargar_categoria/<string:categoria>", methods=['GET'])
@app.route("/realizar_compra/cargar_categoria/<string:categoria>", methods=['POST'])
def redirect_category(categoria):
    return redirect(url_for('category', categoria=categoria))

@app.route("/index/busqueda", methods=['POST'])
def redirect_busqueda():
    global catalogue
    busqueda = request.form['search']
    peliculas = []
    for film in catalogue['peliculas']:
        if busqueda in film['titulo']:
            peliculas.append(film)
    return redirect(url_for('busqueda', movies=peliculas))

@app.route("/realizar_compra/realizar_compra/<string:id>", methods=['POST'])
def redirect_realizar_compra(id):
    return redirect(url_for('realizar_compra', id=id))

@app.route("/introducir_saldo", methods=['POST'])
def introducir_saldo():
    if logged:
        saldo_a_introducir = request.form['input_saldo']
        dir_path = homedir = os.path.expanduser("~")
        dir_path += "/public_html/usuarios/"+username_logged
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
