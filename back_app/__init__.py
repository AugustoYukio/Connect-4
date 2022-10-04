import os
import secrets
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from src.entities.DTO import configure as config_ma
from src.entities.model import configure as config_db


# from .model import configure as config_db
# from .serealizer import configure as config_ma
# app.container
# socketio = SocketIO(app, async_mode="eventlet")
# eventlet.monkey_patch()


def config_bcrypt(app):
    bcrypt = Bcrypt(app)
    return bcrypt


def create_socket(app):
    return SocketIO(app)


basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    template_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src', 'views', 'templates')
    app = Flask(__name__, template_folder=template_path)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////" + os.path.join(basedir, "app.db")
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dbdir/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(45)

    config_db(app)
    config_ma(app)
    config_bcrypt(app)

    Migrate(app, app.db)

    JWTManager(app)

    from .src.usecases.users import bp_user
    app.register_blueprint(bp_user)

    from .src.usecases.home import bp_home

    app.register_blueprint(bp_home)

    return app
