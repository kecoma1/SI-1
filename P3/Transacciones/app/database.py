# -*- coding: utf-8 -*-

import os
import sys, traceback, time
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
import time

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
                WHERE a.customerid = "+str(customerid)+" AND a.orderid = orderdetail.orderid"
    del_2 = "DELETE FROM orders\
                WHERE customerid = "+str(customerid)+""
    del_3 = "DELETE FROM customers WHERE customerid = "+str(customerid)+""

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
        for del_ in lista:
            i+=1

            # Ejecutamos begin
            dbr.append("[info] Begin: en ejecución...")
            if bSQL:
                db_conn.execute("BEGIN")
            else:
                session.begin(subtransactions=True)
            dbr.append("[info] Begin: ¡Ejecutado!")

            # Commit intermedio
            if bCommit:
                dbr.append("[info] Commit (intermedio): en ejecución...")
                if bSQL:
                    db_conn.execute("COMMIT")
                else:
                    session.commit()
                dbr.append("[info] Commit (intermedio): ¡Ejecutado!")

            # Hacemos commit intermedio en caso de fallo
            if bFallo:
                dbr.append("[info] Commit (fallo): en ejecución...")
                if bSQL:
                    db_conn.execute("COMMIT")
                else:
                    session.commit()
                dbr.append("[info] Commit (fallo): ¡Ejecutado!")

            # Ejecutamos la consulta
            dbr.append("[info] Consulta "+str(i)+" de 3: en ejecución...")
            if bSQL:
                db_conn.execute(del_)
            else:
                session.execute(del_)
            # Sleep justo después de la ejecución
            time.sleep(40)
            dbr.append("[info] Consulta "+str(i)+" de 3: ¡Ejecutada!")

            dbr.append("[info] Commit: en ejecución...")
            if bSQL:
                db_conn.execute("COMMIT")
            else:
                session.commit()
            dbr.append("[info] Commit: ¡Ejecutado!")
    except Exception as e:
        print("Exception in DB access:")
        print("-"*60)
        traceback.print_exc(file=sys.stderr)
        print("-"*60)

        dbr.append("[info] Error")
        dbr.append("[info] Error - Rollback: en ejecución...")
        # Hacemos rollback
        if bSQL:
            db_conn.execute("ROLLBACK")
        else:
            session.rollback()
        dbr.append("[info] Error - Rollback: ¡Ejecutado!")

        # Finalizando la transaccion
        dbr.append("[info] Error - END: en ejecución...")
        if bSQL:
            db_conn.execute("END")
        else:
            session.execute("END")
        dbr.append("[info] Error - END: ¡Ejecutado!")
        # Desconexión de la base de datos y sesión sqlalchemy
        dbCloseConnect(db_conn)
        session.close()
    else:
        dbr.append("[info] Ejecución correcta.")

        dbr.append("[info] Finalizando transaccion.")
        # Finalizando la transaccion
        dbr.append("[info] END: en ejecución...")
        if bSQL:
            db_conn.execute("END")
        else:
            session.execute("END")
        dbr.append("[info] END: ¡Ejecutado!")

        # Desconexión de la base de datos y sesión sqlalchemy
        dbCloseConnect(db_conn)
        session.close()
    return dbr

