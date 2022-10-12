from sqlalchemy import Column, DateTime, CheckConstraint, func
from sqlalchemy.orm import backref, relationship
try:
    from back_app.src.entities.model import db
except ImportError:
    from src.entities.model import db


class Theme(db.Model):
    __tablename__ = 'theme'
    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(50), nullable=False)
    price = Column(db.Numeric(5, 2), nullable=False)

    chip1_id = Column(db.Integer, db.ForeignKey("chip.id"), nullable=False)
    chip2_id = Column(db.Integer, db.ForeignKey("chip.id"), nullable=False)
    board_id = Column(db.Integer, db.ForeignKey("board.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    db.UniqueConstraint(chip1_id, chip2_id, board_id)
