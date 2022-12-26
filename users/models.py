from db import db
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime
from recycling_bids.models import Application


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.DateTime)
    rating = db.Column(db.Float, default=0.0, nullable=True)
    is_staff = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    recycling_bids = db.relationship("Application", backref="user", lazy=True)

    # def __init__(self, *args, **kwargs):
    #     self.username = kwargs.get('username')
    #     self.email = kwargs.get('email')
    #     self.password = kwargs.get('password')
    #     self.first_name = kwargs.get('first_name')
    #     self.last_name = kwargs.get('last_name')
    #     self.birthday = kwargs.get('birthday')
    #     self.is_admin = kwargs.get('is_admin', False)
    #     self.is_staff = kwargs.get('is_staff', False)

    def __repr__(self):
        return f"<User: {self.username}>"

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)