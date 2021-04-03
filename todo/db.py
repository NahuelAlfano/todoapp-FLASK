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
    # si db no esta en la variable G

    if 'db' not in g: 
        # creamos una nueva propiedad que contiene la conexion a la base de datos

        g.db = mysql.connector.connect(
            # con current app accedo a las variables creadas en __init__.py de la aplicacion
            host = current_app.config['DATABASE_HOST'],
            user = current_app.config['DATABASE_USER'],
            password = current_app.config['DATABASE_PASSWORD'],
            database = current_app.config['DATABASE']
        )
        
        # creamos otra propiedad que guarda el cursor
        g.c = g.db.cursor(dictionary=True)

    # retorno la base de datos y el cursor cuando llame a get_db
    return g.db, g.c

# funcion para cerrar la conexion por si nos olvidamos despues de realizar una peticion

def close_db(e = None):
    db = g.pop('db', None)
    # si db no se encuentra definido, no hace falta cerrar conexion. si se encuentra, se ejecuta db.close
    if db is not None:
        db.close()

def init_db():
    db, c = get_db()
    for i in instructions:
        c.execute(i)
    
    db.commit()

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Base de datos inicializada')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)