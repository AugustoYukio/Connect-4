import os
import secrets
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_socketio import SocketIO
from back_app import BASE_DIR
from back_app.src.entities.DTO import ma
from back_app.src.entities.model import db

os.environ['FLASK_APP'] = 'app'
os.environ['FLASK_DEBUG'] = 'Development'

bcrypt_flask = Bcrypt()


def config_db(app):
    db.init_app(app)
    bcrypt_flask.init_app(app)
    app.db = db


def config_ma(app):
    ma.init_app(app)


# from .model import configure as config_db
# from .serealizer import configure as config_ma
# app.container
# socketio = SocketIO(app, async_mode="eventlet")
# eventlet.monkey_patch()


def create_socket(app):
    return SocketIO(app)


class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "game_database.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = secrets.token_urlsafe(45)


def create_app():
    template_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src', 'views', 'templates')
    app = Flask(__name__, template_folder=template_path)
    app.config.from_object(Config)
    # app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(basedir, "game_database.db")
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(45)

    config_db(app)
    config_ma(app)

    migrate = Migrate(app=app, db=app.db)
    # with app.app_context() as ctx:
    # ctx.app.db.create_all()
    # manager = Manager(app)

    JWTManager(app)

    from back_app.src.usecases.users import bp_user
    app.register_blueprint(bp_user)

    from back_app.src.usecases.home import bp_home
    app.register_blueprint(bp_home)
    ws = create_socket(app)
    return app, ws
