from datetime import datetime

from flask import jsonify, Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate, init, stamp, migrate, upgrade
import os

from flask_socketio import SocketIO

migration = Migrate()
bcrypt_flask = Bcrypt()
cors = CORS()

try:
    from .src.entities.model import db
    from .src.entities.model.chip import Chip
    from .src.entities.model.board import Board
    from .src.entities.model.theme import Theme
    from .src.entities.model.user import User
    from .src.entities.model.inventory import Inventory
    from .src.utils.messages import MSG_TOKEN_EXPIRED, MSG_INVALID_CREDENTIALS, MSG_PERMISSION_DENIED
    from .src.entities.DTO import ma
    from .config import config
except ImportError:
    from src.entities.model import db
    from src.entities.model.chip import Chip
    from src.entities.model.board import Board
    from src.entities.model.theme import Theme
    from src.entities.model.user import User
    from src.entities.model.inventory import Inventory
    from src.utils.messages import MSG_TOKEN_EXPIRED, MSG_INVALID_CREDENTIALS
    from src.entities.DTO import ma
    from config import config


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
            return {'username': user.username, 'is_active': user.active, 'is_admin': user.admin}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify(
            status=401,
            message=MSG_TOKEN_EXPIRED.format(datetime.utcfromtimestamp(jwt_payload.get('iat')))
        ), 401

    @jwt.unauthorized_loader
    def unauthorized_callback(e):
        resp = jsonify({
            'status': 401,
            'description': e,
            'message': MSG_PERMISSION_DENIED
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

    try:
        from .src.usecases.boards import bp_board
    except ImportError:
        from src.usecases.boards import bp_board
    app.register_blueprint(bp_board)

    try:
        from .src.usecases.inventory import bp_inventory
    except ImportError:
        from src.usecases.inventory import bp_inventory
    app.register_blueprint(bp_inventory)


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
        init(directory=directory)

    stamp(directory=directory)
    migrate(directory=directory)
    upgrade(directory=directory)
