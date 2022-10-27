import os

from sqlalchemy import Column, DateTime, func, event

try:
    from back_app.src.entities.model import db
except ImportError:
    from src.entities.model import db


class Chip(db.Model):
    __tablename__ = 'chip'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), unique=True, nullable=False)
    url = Column(db.String(255), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


@event.listens_for(Chip.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(
        Chip(name="default_1", url=os.getenv('DEFAULT_CHIP1_URL', 'DEFAULT_CHIP1_URL'))
    )
    db.session.add(
        Chip(name="default_2", url=os.getenv('DEFAULT_CHIP2_URL', 'DEFAULT_CHIP2_URL'))
    )
    db.session.commit()
