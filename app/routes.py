#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys
import hashlib
import random

# Catálogo
catalogue = None
catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json')).read()
catalogue = json.loads(catalogue_data)

# Variable booleana para saber si hay un usuario logeado
logged = False

@app.route('/')
@app.route('/index')
@app.route("/index.html", methods=['GET', 'POST'])
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

@app.route("/login.html", methods=['POST'])
def login_page_POST():
    global logged
    if request.form['username']:
        username = request.form['username']
        password = hashlib.sha512((request.form['password']).encode('utf-8')).hexdigest()

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
                session['usuario'] = username
                logged = True
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
        session.pop('usuario', None)
        return redirect(url_for('index'))
    else:
        return render_template('login.html', title='login', logged=logged)


@app.route("/signup.html", methods=['POST'])
def signup_page():
    global logged
    if logged == True:
        return render_template('signup.html', title='signup', logged=logged, error="Cierre sesión por favor")

    if request.form['username']:
        username = request.form['username']
        password = hashlib.sha512((request.form['password_input']).encode('utf-8')).hexdigest()
        card = request.form['card']
        card = card.replace(' ', '')
        wallet = random.randrange(0, 100)

        session['usuario'] = username

        # Comprobamos si existe el usuario
        dir_path = homedir = os.path.expanduser("~")
        dir_path += "/public_html/usuarios/"+username
        if os.path.exists(dir_path):
            return render_template('signup.html', title='signup', logged=logged, error="El usuario ya existe")
        else:
            os.mkdir(dir_path)

            # Creando historial
            f = open(dir_path+"/historial.json","w")
            f.close()

            # Escribiendo los datos
            f = open(dir_path+"/datos.dat","w")
            f.write(username+" "+password+" "+request.form['email']+" "+card+" "+str(wallet))
            f.close()
            
            logged = True
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

@app.route("/index/<id>", methods=['GET'])
def film_detail(id):
    global catalogue, logged
    return render_template('filmDetail.html', film=catalogue['peliculas'][int(id)-1], logged=logged)

# Redirects desde index/<id>   
@app.route("/index/index", methods=['GET'])
@app.route("/index/index.html", methods=['GET'])
def redirect_index():
    return redirect(url_for('index'))

@app.route("/index/login.html", methods=['GET'])
def redirect_login_page():
    return redirect(url_for('login_page_GET'))

@app.route("/index/signup.html", methods=['GET'])
def redirect_signup_page():
    return redirect(url_for('signup_page_get'))

@app.route("/index/topnav.html", methods=['GET'])
def redirect_topnav():
    return render_template('topnav.html', logged=logged)

@app.route("/index/sidenav.html", methods=['GET'])
def redirect_sidenav():
    return render_template('sidenav.html', logged=logged)