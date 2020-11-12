#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, session
import os
import sys

app = Flask(__name__)

# ejemplo de sesion Flask: http://flask.pocoo.org/docs/1.0/quickstart/#sessions
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

try:
    from flask_session import Session
    this_dir = os.path.dirname(os.path.abspath(__file__))
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = this_dir + '/thesessions'
    SESSION_COOKIE_NAME = 'flasksessionid'
    # Numero maximo de elementos de sesion guardados antes de borrar alguno, por defecto = 500
    SESSION_FILE_THRESHOLD = 10
    app.config.from_object(__name__)
    #app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    Session(app)
    print ("Usando sesiones de Flask-Session en fichero del servidor", file=sys.stderr)
except ImportError as e:
    print ("Flask-Session no disponible, usando sesiones de Flask en cookie", file=sys.stderr)

from app import routes, database
