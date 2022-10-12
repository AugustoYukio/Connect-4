from sqlalchemy import Column, DateTime, CheckConstraint, func
from sqlalchemy.orm import backref, relationship
try:
    from back_app.src.entities.model import db, bcrypt_flask
except ImportError:
    from src.entities.model import db, bcrypt_flask


class Book(db.Model):
    __tablename__ = "books"
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String)
    author_id = Column(db.Integer, db.ForeignKey("authors.id"))
    author = relationship("Author", backref=backref("books"))


class Author(db.Model):
    __tablename__ = "authors"
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)

    def __repr__(self):
        return "<Author(name={self.name!r})>".format(self=self)


class User(db.Model):
    __tablename__ = 'user'
    id = Column(db.Integer, primary_key=True, autoincrement=True)

    # User Authentication fields
    username = Column(db.String(50), nullable=False, unique=True)
    email_confirmed_at = Column(db.DateTime())
    password = Column(db.String(255), nullable=False)

    # User generic data
    secondary_email = Column(db.String(255), nullable=True, unique=True)
    principal_email = Column(db.String(255), nullable=False, unique=True)
    avatar_url = Column(db.String(255), nullable=True, unique=False)
    default_theme = Column(db.Integer, CheckConstraint('default_theme>0'))
    admin = Column(db.Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # User fields
    active = Column(db.Boolean())
    first_name = Column(db.String(50), nullable=False)
    # NOT NULL
    last_name = Column(db.String(50), nullable=False)

    def gen_hash(self):
        self.password = bcrypt_flask.generate_password_hash(self.password).decode('utf8')

    def verify_password(self, password):
        return bcrypt_flask.check_password_hash(self.password, password)

    def __repr__(self):
        return f"{self.first_name} - {self.last_name}"

    def is_active(self):
        return self.active

    def is_admin(self):
        return self.admin
