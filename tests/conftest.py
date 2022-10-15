from os.path import join
from datetime import timedelta

import ipdb
from flask_jwt_extended import create_access_token, create_refresh_token
from pytest import fixture
from back_app.factory import check_and_upgrade_all_tables


# from back_app.factory import create_app


@fixture()
def app():
    from back_app.factory import create_app
    app = create_app('testing')[0]
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here
    # ipdb.set_trace()
    check_and_upgrade_all_tables(app, directory=join(app.root_path, app.extensions['migrate'].directory))
    yield app


@fixture()
def client(app):
    return app.test_client()


@fixture()
def runner(app):
    return app.test_cli_runner()


@fixture(scope='function')
def user_db():
    from back_app.src.entities.model.user import User
    return User


@fixture(scope='function')
def chip_db():
    from back_app.src.entities.model.chip import Chip
    return Chip


@fixture(scope='function')
def theme_db():
    from back_app.src.entities.model.theme import Theme
    return Theme


@fixture(scope='function')
def unauthenticated_headers():
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    return headers


@fixture
def header_with_access_token(app, client):
    acess_token = create_access_token(identity=1, expires_delta=timedelta(days=5))
    refresh_token = create_refresh_token(identity=1)
    return {
        'Authorization': f'Bearer {acess_token}',
        'Content-Type': 'application/json'
    }
