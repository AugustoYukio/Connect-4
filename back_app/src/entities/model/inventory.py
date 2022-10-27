from sqlalchemy import event

try:
    from back_app.src.entities.model import db
except ImportError:
    from src.entities.model import db


class Inventory(db.Model):
    __tablename__ = 'inventory'
    __table_args__ = (
        db.UniqueConstraint('user_id', 'theme_id', name="fk_user_id_theme_id"),
        )
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    theme_id = db.Column(db.Integer, db.ForeignKey("theme.id"), nullable=False, primary_key=True)

    def __repr__(self):
        return f"User ID: {self.user_id} - Theme ID: {self.theme_id}"


@event.listens_for(Inventory.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    inventory = Inventory(theme_id=0, user_id=0)
    db.session.add(inventory)
    db.session.commit()
