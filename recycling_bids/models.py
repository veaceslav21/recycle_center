from db import db
from users.models import User
from centers.models import Center
import datetime
from enum import Enum


class MaterialType(Enum):
    GLASS = "glass"
    PAPER = "paper"
    PLASTIC = "plastic"


class Application(db.Model):
    """
    Class describe what a recycle request should contain
    """

    id = db.Column(db.Integer, primary_key=True)
    material_type = db.Column(db.Enum(MaterialType, values_callable=lambda x: [item.value for item in MaterialType]))
    capacity = db.Column(db.Float, nullable=True)
    center_id = db.Column(db.Integer, db.ForeignKey(Center.id), nullable=False)
    user_id = db.relationship(db.Integer, db.ForeignKey(User.id), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=True)
