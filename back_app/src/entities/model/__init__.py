from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt_flask = Bcrypt()

db = SQLAlchemy(session_options={"expire_on_commit": False})


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()



