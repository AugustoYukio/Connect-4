from datetime import timedelta
from os import getenv, path, getcwd
import secrets

BASE_PATH = path.dirname(path.realpath(__file__))

LOCAL_DATABASE_URI = path.join(BASE_PATH, "game_database.db")


class Config:
    SECRET_KEY = getenv('SECRET_KEY', secrets.token_urlsafe(45))
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY', secrets.token_urlsafe(45))
    PORT = int(getenv('PORT', 5000))
    DEBUG = getenv('DEBUG') or False
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', f"sqlite:///{LOCAL_DATABASE_URI}")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=int(getenv('JWT_ACCESS_TOKEN_EXPIRES', 120))
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=int(getenv('JWT_REFRESH_TOKEN_EXPIRES', 30))
    )


class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    FLASK_ENV = 'testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', f"sqlite:///{LOCAL_DATABASE_URI}")


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    TESTING = False
    DEBUG = False


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
