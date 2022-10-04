from . import db, Column


class Chip(db.Model):
    __tablename__ = 'chip'

    id = Column(db.Inter, primary_key=True)
    name = Column(db.String(50), unique=True)
    url = Column(db.String(255), unique=True)

