import os

import ipdb
from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, upgrade, migrate, init, stamp
from flask_socketio import SocketIO
from flask_cors import CORS

try:
    from .src.entities.model.user import User
    from .src.entities.model.theme import Theme
    from .src.entities.model.board import Board
    from .src.entities.model.chip import Chip
    from .src.utils.messages import MSG_TOKEN_EXPIRED, MSG_INVALID_CREDENTIALS
    from .src.entities.model import db
    from .src.entities.DTO import ma
    from .config import config
except ImportError:
    from src.entities.model.user import User
    from src.entities.model.theme import Theme
    from src.entities.model.board import Board
    from src.entities.model.chip import Chip
    from src.utils.messages import MSG_TOKEN_EXPIRED, MSG_INVALID_CREDENTIALS
    from src.entities.model import db
    from src.entities.DTO import ma
    from config import config

migration = Migrate()

bcrypt_flask = Bcrypt()

cors = CORS()


def config_db(app):
    db.init_app(app)
    bcrypt_flask.init_app(app)
    app.db = db


def configure_migration(app):
    migration.init_app(app=app, db=app.db)


def configure_cors(app):
    cors.init_app(app)


def configure_jwt(app):
    # Add jwt handler
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_access_token(user_id):
        user = User.query.get(user_id)

        # Podemos extender as informações do usuaŕio adicionando
        # novos campos: active, roles, full_name e etc...

        if user:
            return {
                'username': user.username,
                'is_active': user.active,
                'is_admin': user.admin
            }

    @jwt.expired_token_loader
    def my_expired_token_callback():
        resp = jsonify({
            'status': 401,
            'sub_status': 42,
            'message': MSG_TOKEN_EXPIRED
        })

        resp.status_code = 401

        return resp

    @jwt.unauthorized_loader
    def my_unauthorized_callback(e):
        resp = jsonify({
            'status': 401,
            'sub_status': 1,
            'description': e,
            'message': MSG_INVALID_CREDENTIALS
        })

        resp.status_code = 401

        return resp


def config_ma(app):
    ma.init_app(app)


# from .model import configure as config_db
# from .serealizer import configure as config_ma
# app.container
# socketio = SocketIO(app, async_mode="eventlet")
# eventlet.monkey_patch()


def create_socket(app):
    return SocketIO(app, async_mode="eventlet")


def configure_blueprint(app):
    try:
        from .src.usecases.users import bp_user
    except ImportError:
        from src.usecases.users import bp_user
    # import ipdb;ipdb.set_trace()
    app.register_blueprint(bp_user)
    try:
        from .src.usecases.home import bp_home
    except ImportError:
        from src.usecases.home import bp_home
    app.register_blueprint(bp_home)

    try:
        from .src.usecases.chips import bp_chip
    except ImportError:
        from src.usecases.chips import bp_chip
    app.register_blueprint(bp_chip)

    try:
        from .src.usecases.themes import bp_theme
    except ImportError:
        from src.usecases.themes import bp_theme
    app.register_blueprint(bp_theme)


def create_app(config_name=os.getenv('FLASK_ENV'), name='back_app'):
    template_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src', 'views', 'templates')
    app = Flask(name, template_folder=template_path)

    app.config.from_object(config[config_name])
    config_db(app)
    config_ma(app)
    configure_migration(app)

    configure_jwt(app)
    configure_blueprint(app)
    configure_cors(app)
    ws = create_socket(app)
    return app, ws


def check_and_upgrade_all_tables(app, directory=None):
    app.app_context().push()

    # create database and tables
    app.db.create_all()
    # ipdb.set_trace()
    if directory is None:
        directory = os.path.join(app.root_path, app.extensions['migrate'].directory)
    # checa se o diretório migrations já foi inicializado
    if not (os.access(directory, os.F_OK) and os.listdir(directory)):
        init()

    stamp(directory=directory)
    migrate(directory=directory)
    upgrade(directory=directory)
