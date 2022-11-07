import os
from datetime import datetime
from sqlalchemy import event

try:
    from back_app.src.entities.model import db, bcrypt_flask
except ImportError:
    from . import db, bcrypt_flask


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = (
        db.CheckConstraint('LENGTH(username) >= 10', name='username_must_minimum_length_10_characters'),
        db.CheckConstraint('secondary_email!=principal_email', name='check_emails_must_different'),
        db.CheckConstraint('LENGTH(principal_email) >= 10', name='principal_email_must_minimum_length'),
        db.CheckConstraint('LENGTH(secondary_email) >= 10', name='secondary_email_must_minimum_length'),
    )
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email_confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False)
    principal_email = db.Column(db.String(255), nullable=False, unique=True)
    secondary_email = db.Column(db.String(255), nullable=True, unique=True)
    avatar_url = db.Column(db.String(255), nullable=True, unique=False)
    current_theme = db.Column(db.Integer, db.ForeignKey("theme.id"), default=0)

    admin = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=db.func.now())
    active = db.Column(db.Boolean(), default=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def gen_hash(self):
        self.password = bcrypt_flask.generate_password_hash(self.password).decode('utf8')

    def verify_password(self, password):
        return bcrypt_flask.check_password_hash(self.password, password)

    def __repr__(self):
        return f"{self.first_name} - {self.last_name}"

    def is_active(self):
        return self.active

    def is_admin(self):
        return self.admin


@event.listens_for(User.__table__, 'after_create')
def insert_root_user(*args, **kwargs):
    super_user = User(
        id=0,
        username='super_admin',
        password=os.getenv('SUPER_ADMIN_PWD', 'SUPER_ADMIN_PWD'),
        principal_email="super_admin@connect4.com.br",
        secondary_email="super_admin2@connect4.com.br",
        admin=True,
        active=True,
        first_name='super user',
        last_name="admin",
        current_theme=0,
        email_confirmed_at=datetime.utcnow()
    )
    super_user.gen_hash()
    db.session.add(super_user)
    db.session.commit()
