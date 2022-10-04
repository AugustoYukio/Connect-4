from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint, Column,  DateTime

db = SQLAlchemy()
bcrypt_flask = Bcrypt()


def configure(app):
    db.init_app(app)
    app.db = db
