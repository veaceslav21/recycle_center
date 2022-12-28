from db import db
import datetime


class Application(db.Model):
    """
    Class describe what a recycle request should contain
    """

    id = db.Column(db.Integer, primary_key=True)
    material_type = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Float, nullable=True)
    center_id = db.Column(db.Integer, db.ForeignKey('center.id'))
    user_id = db.relationship(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now(), nullable=True)

    def __repr__(self):
        return f"Request: {self.material_type}, {self.capacity} kg"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
