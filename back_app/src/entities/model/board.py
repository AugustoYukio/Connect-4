from sqlalchemy import Column, DateTime, CheckConstraint, func
from sqlalchemy.orm import backref, relationship
try:
    from back_app.src.entities.model import db
except ImportError:
    from src.entities.model import db


class Board(db.Model):
    __tablename__ = 'board'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), unique=True, nullable=False)
    url = Column(db.String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
