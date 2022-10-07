from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from sqlalchemy import CheckConstraint, Column,  DateTime
from sqlalchemy.orm import relationship, backref
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt_flask = Bcrypt()

db = SQLAlchemy()
