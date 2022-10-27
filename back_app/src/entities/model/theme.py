import os

from sqlalchemy import Column, DateTime, CheckConstraint, func, event
from sqlalchemy.orm import backref, relationship

try:
    from back_app.src.entities.model import db
except ImportError:
    from src.entities.model import db


class Theme(db.Model):
    __tablename__ = 'theme'
    __table_args__ = (db.CheckConstraint('chip1_id != chip2_id', name='chips_in_themes_must_be_different'),)

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), nullable=False, unique=True)
    price = Column(db.Numeric(5, 2), nullable=False)

    chip1_id = Column(db.Integer, db.ForeignKey("chip.id", ondelete=u'CASCADE'), nullable=False)
    chip2_id = Column(db.Integer, db.ForeignKey("chip.id", ondelete=u'CASCADE'), nullable=False)
    board_id = Column(db.Integer, db.ForeignKey("board.id", ondelete=u'CASCADE'), nullable=False)
    image = Column(db.String(150), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    inventory_items = db.relationship('Inventory', backref='theme')


@event.listens_for(Theme.__table__, 'after_create')
def insert_default_theme(*args, **kwargs):
    db.session.add(
        Theme(
            id=0, name=r'default', price=0, chip1_id=1, chip2_id=2, board_id=0, image=os.getenv(
                'DEFAULT_THEME_IMAGE', 'DEFAULT_THEME_IMAGE')
        )
    )
    db.session.commit()
