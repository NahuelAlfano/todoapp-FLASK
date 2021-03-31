import mysql.connector
# click es una herramienta para ejecutar comandos en terminal creando tablas y relacion sin mysqlWorkbecn

import click

# current_app mantiene la app que se esta ejecutando y g es una variable que se puede reasignar y reutilizar. lo usamos para almacenar al usuario
from flask import current_app, g

# with_appcontext importa las variables de la aplicacion para usar
from flask.cli import with_appcontext

# contiene los scripts para crear la base de datos
from .schema import instructions



def get_db():
    if 'db' not in g: 
        g.db = mysql.connector.connect(
            host = current_app.config['DATABASE_HOST'],
            user = current_app.config['DATABASE_USER'],
            password = current_app.config['DATABASE_PASSWORD'],
            database = current_app.config['DATABASE']
        )

        g.c = g.db.cursor(dictionary=True)

    return g.db, g.c

def close_db(e = None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    app.teardown_appcontext(close_db)