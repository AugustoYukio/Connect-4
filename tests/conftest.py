from pytest import fixture


# from back_app.factory import create_app


@fixture()
def app():
    from back_app.factory import create_app
    app = create_app('testing')[0]
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

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
def unauthenticated_headers():
    mimetype = 'application/json'
    headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
    return headers
