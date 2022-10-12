from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt_flask = Bcrypt()

db = SQLAlchemy(session_options={"expire_on_commit": False})

