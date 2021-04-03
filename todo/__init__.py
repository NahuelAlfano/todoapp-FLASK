import os
from flask import Flask


def create_app():
    app = Flask(__name__)

    # config.from.mapping permite establecer variables de la app
    app.config.from_mapping(
        SECRET_KEY = 'naja',
        DATABASE_HOST = os.environ.get('FLASK_DATABASE_HOST'),
        DATABASE_PASSWORD = os.environ.get('FLASK_DATABASE_PASSWORD'),
        DATABASE_USER = os.environ.get('FLASK_DATABASE_USER'),
        DATABASE = os.environ.get('FLASK_DATABASE')
    )

    # importo todo lo que hay en el archivo db
    from . import db

    # le paso como parametro la app, para que despues de realizar la peticion, se ejecute el teardown_appcontext
    db.init_app(app)

    @app.route('/hola')
    def hola():
        return 'Chanchito Feliz'

    return app