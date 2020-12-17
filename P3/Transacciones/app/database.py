# -*- coding: utf-8 -*-

import os
import sys, traceback, time
from sqlalchemy import create_engine

# configurar el motor de sqlalchemy
db_engine = create_engine("postgresql://alumnodb:alumnodb@localhost/si1", echo=False, execution_options={"autocommit":False})

def dbConnect():
    return db_engine.connect()

def dbCloseConnect(db_conn):
    db_conn.close()

def getMovies(anio):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select movietitle from imdb_movies where year = '" + anio + "'"
    resultproxy=db_conn.execute(query)

    a = []
    for rowproxy in resultproxy:
        d={}
        # rowproxy.items() returns an array like [(key0, value0), (key1, value1)]
        for tup in rowproxy.items():
            # build up the dictionary
            d[tup[0]] = tup[1]
        a.append(d)
        
    resultproxy.close()  
    
    db_conn.close()  
    
    return a
    
def getCustomer(username, password):
    # conexion a la base de datos
    db_conn = db_engine.connect()

    query="select * from customers where username='" + username + "' and password='" + password + "'"
    res=db_conn.execute(query).first()
    
    db_conn.close()  

    if res is None:
        return None
    else:
        return {'firstname': res['firstname'], 'lastname': res['lastname']}
    
def delCustomer(customerid, bFallo, bSQL, duerme, bCommit):

    # Array de trazas a mostrar en la página
    dbr=[]

    del_1 = "DELETE FROM orderdetail\
                USING orders AS a\
                WHERE a.customerid = 1 AND a.orderid = orderdetail.orderid"
    del_2 = "DELETE FROM orders\
                WHERE customerid = 1"
    del_3 = "DELETE FROM customers WHERE customerid = 1"

    # Creamos una lista para poder iterar sobre las consultas
    if bFallo:
        lista = [del_2, del_3, del_1]
    else:
        lista = [del_1, del_2, del_3]

    # Conexión con la base de datos
    db_conn = None
    db_conn = dbConnect()

    # Sesión para las transaciones SQLAlchemy
    session = None
    Session = sessionmaker(bind=db_engine)
    session = Session()

    try:
        i = 0
        # Ejecutamos con fallo
        for del_ in lista:
            i+=1

            # Ejecutamos begin
            dbr.append("[info] Begin: en ejecución...")
            if bSQL:
                db_conn.execute("BEGIN")
            else:
                session.begin()
            dbr.append("[info] Begin: ¡Ejecutado!")

            # Commit intermedio
            if bCommit:
                dbr.append("[info] Commit: en ejecución...")
                if bSQL:
                    db_conn.execute("COMMIT")
                else:
                    session.commit()
                dbr.append("[info] Commit: ¡Ejecutado!")

            # Hacemos commit intermedio en caso de fallo
            if bFallo:
                dbr.append("[info] Commit: en ejecución...")
                if bSQL:
                    db_conn.execute("COMMIT")
                else:
                    session.commit()
                dbr.append("[info] Commit: ¡Ejecutado!")

            # Ejecutamos la consulta
            dbr.append("[info] Consulta "+i+" de 3: en ejecución...")
            if bSQL:
                db_conn.execute(del_)
            else:
                session.execute(del_)
            dbr.append("[info] Consulta "+i+" de 3: ¡Ejecutada!")

            dbr.append("[info] Commit: en ejecución...")
            if bSQL:
                db_conn.execute("COMMIT")
            else:
                session.commit()
            dbr.append("[info] Commit: ¡Ejecutado!")
    except Exception as e:
        dbr.append("[info] Error")
        dbr.append("[info] Rollback: en ejecución...")
        # Hacemos rollback
        if bSQL:
            db_conn.execute("ROLLBACK")
        else:
            session.rollback()
        dbr.append("[info] Rollback: ¡Ejecutado!")
        # Desconexión de la base de datos y sesión sqlalchemy
        dbCloseConnect(db_conn)
        session.close()
    else:
        dbr.append("[info] Ejecución correcta")
        dbCloseConnect(db_conn)
        session.close()
    return dbr

