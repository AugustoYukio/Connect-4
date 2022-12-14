import os
from sqlalchemy import Column, DateTime, CheckConstraint, func, event

try:
    from back_app.src.entities.model import db
except ImportError:
    from . import db


class Board(db.Model):
    __tablename__ = 'board'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), unique=True, nullable=False)
    url = Column(db.String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


@event.listens_for(Board.__table__, 'after_create')
def insert_default_board(*args, **kwargs):
    db.session.add(Board(id=0, name=r'default', url=os.getenv('DEFAULT_BOARD_URL', 'DEFAULT_BOARD_URL')))
    db.session.commit()


