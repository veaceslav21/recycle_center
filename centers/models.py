from db import db
from recycling_bids.models import Application


class Center(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), unique=True, nullable=False)
    # types of materials
    glass = db.Column(db.Boolean)
    plastic = db.Column(db.Boolean)
    paper = db.Column(db.Boolean)
    recycling_bids = db.relationship(Application, backref="center")

    def __repr__(self):
        return f"Center: {self.address}"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
