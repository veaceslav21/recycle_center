from db import db
from flask_bcrypt import generate_password_hash, check_password_hash
import datetime
from recycling_bids.models import Application


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), index=True, unique=True, nullable=False)
    email = db.Column(db.String(80), index=True, unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birthday = db.Column(db.DateTime)
    rating = db.Column(db.Float, default=0.0, nullable=True)
    points = db.Column(db.Integer, default=0, nullable=True)
    request_count = db.Column(db.Integer, default=0, nullable=True)
    is_staff = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    recycling_bids = db.relationship(Application, backref="user")

    def __repr__(self):
        return f"<User: {self.username}>"

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)
