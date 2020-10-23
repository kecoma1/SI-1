#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from flask import render_template, request, url_for, redirect, session
import json
import os
import sys

# Catálogo
catalogue = None
catalogue_data = open(os.path.join(app.root_path,'catalogue/catalogue.json'), encoding="utf-8").read()
catalogue = json.loads(catalogue_data)

# Variable booleana para saber si hay un usuario logeado
logged = False

@app.route('/')
@app.route('/index')
@app.route("/index.html", methods=['GET', 'POST'])
def index():
    global catalogue, logged
    return render_template('index.html', movies=catalogue['peliculas'], logged=logged)

@app.route('/login', methods=['GET', 'POST'])
def login():
    global logged
    # doc sobre request object en http://flask.pocoo.org/docs/1.0/api/#incoming-request-data
    if 'username' in request.form:
        # aqui se deberia validar con fichero .dat del usuario
        if request.form['username'] == 'pp':
            session['usuario'] = request.form['username']
            session.modified=True
            # se puede usar request.referrer para volver a la pagina desde la que se hizo login
            return redirect(url_for('index'))
        else:
            # aqui se le puede pasar como argumento un mensaje de login invalido
            return render_template('login.html', title = "Sign In", logged=logged)
    else:
        # se puede guardar la pagina desde la que se invoca 
        session['url_origen']=request.referrer
        session.modified=True        
        # print a error.log de Apache si se ejecuta bajo mod_wsgi
        print (request.referrer, file=sys.stderr)
        return render_template('login.html', title = "Sign In", logged=logged)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    global logged
    session.pop('usuario', None)
    return redirect(url_for('index'))

# Rutas a las diferentes páginas
@app.route("/index/sidenav.html", methods=['GET'])
@app.route("/sidenav.html", methods=['GET'])
def sidenav():
    global logged
    return render_template('sidenav.html', logged=logged)

@app.route("/index/topnav.html", methods=['GET'])
@app.route("/topnav.html", methods=['GET'])
def topnav():
    global logged
    return render_template('topnav.html', logged=logged)

@app.route("/login.html", methods=['GET'])
def login_page():
    global logged
    return render_template('login.html', title='login', logged=logged)

@app.route("/signup.html", methods=['POST'])
def signup_page():
    global logged
    if request.form['username']:
        username = request.form['username']
        session['usuario'] = username
        session['password_input'] = request.form['password_input']
        session['email'] = request.form['email']
        session['card'] = request.form['card']

        # Comprobamos si existe el usuario
        dir_path = homedir = os.path.expanduser("~")
        dir_path += "/public_html/usuarios/"+username
        if os.path.exists(dir_path):
            return render_template('signup.html', title='signup', logged=logged, error="El usuario ya existe")
        else:
            os.mkdir(dir_path)
            f = open(dir_path+"/historial.json","w")
            f.close()
            f = open(dir_path+"/datos.dat","w")
            f.close()
            logged = True
            return redirect(url_for('index'))
    else:
        return render_template('signup.html', title='signup', logged=logged, error="Los datos no fueron introducidos correctamente")

@app.route("/signup.html", methods=['GET'])
def signup_page_get():
    global logged
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
    return redirect(url_for('login_page'))

@app.route("/index/signup.html", methods=['GET'])
def redirect_signup_page():
    return redirect(url_for('signup_page'))